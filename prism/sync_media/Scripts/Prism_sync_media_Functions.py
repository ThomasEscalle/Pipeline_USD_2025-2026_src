
# -*- coding: utf-8 -*-

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher_plugin as err_catcher

import os
import json
import shutil

import time
import traceback

#LOG_FILE = os.path.join("D:/tempLog", "prism_sync_media.log")

#def log(msg):
#    with open(LOG_FILE, "a") as f:
#        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")

# =========================================================
# WORKER
# =========================================================
class RuleSelectionDialog(QDialog):

    def __init__(self, rules, parent=None):

        super().__init__(parent)
        #log("OPEN RULE SELECTION DIALOG")

        self.setWindowTitle("Select Sync Rules")
        self.resize(500, 300)
        self.rules = rules
        self.checkboxes = []

        layout = QVBoxLayout(self)

        label = QLabel("Select rules to synchronize:")
        layout.addWidget(label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        scrollWidget = QWidget()

        scrollLayout = QVBoxLayout(scrollWidget)
        scrollLayout.setContentsMargins(5, 5, 5, 5)
        scrollLayout.setSpacing(5)

        for rule in rules:
            source_media = rule.get("source_media", [])
            if isinstance(source_media, str):
                source_media = [source_media]

            if source_media:
                rule_name = source_media[0]
            else:
                rule_name = "Unnamed Rule"

            checkbox = QCheckBox(rule_name)
            checkbox.setChecked(True)

            scrollLayout.addWidget(checkbox)

            self.checkboxes.append((checkbox, rule))

        scrollLayout.addStretch()

        scrollWidget.setLayout(scrollLayout)

        scroll.setWidget(scrollWidget)

        layout.addWidget(scroll)
        # buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def getSelectedRules(self):

        selected = []

        for checkbox, rule in self.checkboxes:

            if checkbox.isChecked():
                selected.append(rule)

        return selected

class SyncWorker(QObject):

    progressChanged = Signal(int)
    statusChanged = Signal(str)
    totalComputed = Signal(int)
    finished = Signal()
    error = Signal(str)

    def __init__(self, core, pipeline_path, rules):
        super().__init__()

        self.core = core
        self.pipeline_path = pipeline_path
        self.rules = rules

        self.cancelled = False

        self.supportedFormats = [
            ".jpg",
            ".jpeg",
            ".JPG",
            ".png",
            ".PNG",
            ".tif",
            ".tiff",
            ".tga",
            ".dpx",
            ".exr",
            ".hdr",
            ".mp4",
            ".mov",
            ".avi",
            ".m4v",
        ]

        self.videoFormats = [".mp4", ".mov", ".avi", ".m4v"]

    def cancel(self):
        self.cancelled = True

    # =====================================================
    # MAIN
    # =====================================================

    def run(self):
        #log("WORKER STARTED")
        try:

            # ---------------------------------------------
            # PHASE 1 : BUILD FILE LIST
            # ---------------------------------------------

            files_to_copy = []
            #log("GET SHOTS")
            shots = self.core.entities.getShots()
            #log(f"SHOT COUNT: {len(shots)}")
            for rule in self.rules:

                source_media = rule["source_media"]

                if isinstance(source_media, str):
                    source_media = [source_media]

                destination = rule["destination"]

                images_destination = destination["images_destination"]
                videos_destination = destination["videos_destination"]

                for i, shot in enumerate(shots):

                    if self.cancelled:
                        #log("WORKER CANCELLED DURING SCANNING")
                        self.finished.emit()
                        return

                    if i % 10 == 0:
                        self.statusChanged.emit(f"Scanning shots... ({i}/{len(shots)})")

                    sequence = shot["sequence"]
                    shot_name = shot["shot"]
                    shot_display_name = sequence + "_" + shot_name

                    path = shot.get("path", "")
                    path = path.replace("\\", "/")

                    search_paths = [
                        os.path.join(path, "Playblasts"),
                        os.path.join(path, "Renders/2dRender"),
                        os.path.join(path, "Renders/3dRender"),
                    ]

                    subdirs = []

                    for p in search_paths:

                        p = p.replace("\\", "/")

                        if not os.path.exists(p):
                            continue

                        for entry in os.listdir(p):

                            full_path = os.path.join(p, entry)

                            if os.path.isdir(full_path):
                                subdirs.append(full_path.replace("\\", "/"))

                    for media_path in subdirs:

                        media_source = os.path.basename(media_path)

                        match = any(
                            sm.lower() == media_source.lower()
                            for sm in source_media
                        )

                        if not match:
                            continue

                        versions = []

                        for entry in os.listdir(media_path):

                            full_path = os.path.join(media_path, entry)

                            if (
                                os.path.isdir(full_path)
                                and entry.startswith("v")
                            ):
                                versions.append(
                                    full_path.replace("\\", "/")
                                )

                        if not versions:
                            continue

                        versions.sort()

                        latest_version_path = versions[-1]

                        for entry in os.listdir(latest_version_path):

                            source_file = os.path.join(
                                latest_version_path,
                                entry
                            )

                            if not os.path.isfile(source_file):
                                continue

                            _, ext = os.path.splitext(entry)

                            if ext not in self.supportedFormats:
                                continue

                            is_video = ext in self.videoFormats

                            destination_template = (
                                videos_destination
                                if is_video
                                else images_destination
                            )

                            destination_file = self.buildDestination(
                                source_file,
                                destination_template,
                                shot_display_name,
                                ext,
                                shot_name,
                                sequence,
                                is_video
                            )

                            files_to_copy.append(
                                (source_file, destination_file, source_media)
                            )

            # ---------------------------------------------
            # PHASE 2 : COPY FILES
            # ---------------------------------------------

            total = len(files_to_copy)

            if total == 0:
                self.finished.emit()
                return
            
            self.totalComputed.emit(total)
            #log(f"FILES TO COPY: {total}")

            update_interval = max(1, total // 100)
            for index, (src, dst, source_media) in enumerate(files_to_copy):
                if self.cancelled:
                    self.finished.emit()
                    return


                self.copyIfNewer(src, dst)

                if index % update_interval == 0 or index == total - 1:
                    self.statusChanged.emit(
                        f"[{source_media}] Copying: {os.path.basename(src)}"
                    )
                    self.progressChanged.emit(index + 1)
                    #log(f"COPY PROGRESS: {index + 1}/{total}")

            #log("WORKER FINISHED COPYING")
            self.finished.emit()

        except Exception as e:
            self.error.emit(str(e))
            self.finished.emit()

    # =====================================================
    # DESTINATION
    # =====================================================

    def buildDestination(
        self,
        source_file,
        destination_template,
        shot_display_name,
        ext,
        shot_name,
        sequence,
        video=False
    ):

        destination = destination_template

        if not video:

            frame_number = (
                self.core.media.getFrameNumberFromFilename(
                    source_file
                )
            )

            destination = destination.replace(
                "@frames@",
                str(frame_number)
            )

        pipeline_cd_up = os.path.dirname(self.pipeline_path)

        destination = destination.replace(
            "@ext@",
            ext.lstrip(".")
        )

        destination = destination.replace(
            "@sht@",
            shot_name
        )

        destination = destination.replace(
            "@seq@",
            sequence
        )

        destination = destination.replace(
            "@shot_display_name@",
            shot_display_name
        )

        destination = destination.replace(
            "@pipeline@",
            pipeline_cd_up.replace("\\", "/")
        )

        return destination

    # =====================================================
    # COPY
    # =====================================================

    def copyIfNewer(self, source_file, destination):
        destination_dir = os.path.dirname(destination)

        try:
            os.makedirs(destination_dir, exist_ok=True)
        except Exception as e:
            #log(f"MAKEDIRS FAILED: {destination_dir} — {e}")
            return

        try:
            if os.path.exists(destination):
                src_time = os.path.getmtime(source_file)
                dst_time = os.path.getmtime(destination)
                if dst_time >= src_time:
                    #☻#log(f"SKIP (up to date): {source_file}")
                    return
        except Exception as e:
            #log(f"MTIME FAILED: {source_file} — {e}")
            return

        ##log(f"COPY: {source_file}")
        try:
            CHUNK = 8 * 1024 * 1024  # 8 MB
            with open(source_file, "rb") as src_f, \
                open(destination, "wb") as dst_f:
                while True:
                    if self.cancelled:
                        break
                    chunk = src_f.read(CHUNK)
                    if not chunk:
                        break
                    dst_f.write(chunk)
                    # PAS de fsync — trop lent sur réseau

            shutil.copystat(source_file, destination)

            if self.cancelled and os.path.exists(destination):
                os.remove(destination)

        except Exception as e:
            #log(f"COPY FAILED: {source_file} — {e}")
            if os.path.exists(destination):
                os.remove(destination)


# =========================================================
# MAIN PLUGIN
# =========================================================

class Prism_sync_media_Functions(object):

    def __init__(self, core, plugin):

        self.core = core
        self.plugin = plugin

        self.core.registerCallback(
            "onProjectBrowserStartup",
            self.onProjectBrowserStartup,
            plugin=self
        )

    # =====================================================
    # MENU
    # =====================================================

    def onProjectBrowserStartup(self, origin):

        origin.syncMenu = QMenu("Sync Media")

        action = origin.syncMenu.addAction(
            "Synchronize",
            self.onActionTriggered
        )

        action.setShortcut(QKeySequence("Ctrl+Shift+W"))

        origin.menubar.addMenu(origin.syncMenu)

    # =====================================================
    # ACTION
    # =====================================================

    def onActionTriggered(self):
        #log("=== ACTION START ===")
        self.pipeline_path = (
            self.core.projects.getResolvedProjectStructurePath(
                "pipeline",
                context={}
            )
        )
        json_settings_path = os.path.join(
            self.pipeline_path,
            "sync_media_settings.json"
        )

        if not os.path.exists(json_settings_path):

            default_settings = {
                "rules": []
            }

            with open(json_settings_path, "w") as f:
                json.dump(default_settings, f, indent=4)

        with open(json_settings_path, "r") as f:
            settings = json.load(f)

        rules = settings.get("rules", [])

        if not rules:
            QMessageBox.information(
                None,
                "Sync Media",
                "No rules found."
            )

            return

        # ==========================================
        # RULE SELECTION DIALOG
        # ==========================================

        dialog = RuleSelectionDialog(rules)

        result = dialog.exec_()

        if result != QDialog.Accepted:
            return

        selected_rules = dialog.getSelectedRules()

        if not selected_rules:

            QMessageBox.information(
                None,
                "Sync Media",
                "No rules selected."
            )

            return

        # =================================================
        # UI
        # =================================================

        self.progress = SyncProgressDialog()
        self.progress.setWindowModality(Qt.NonModal)
        self.progress.show()


        # =================================================
        # THREAD
        # =================================================

        self.thread = QThread()

        self.worker = SyncWorker(
            self.core,
            self.pipeline_path,
            selected_rules
        )

        self.progress.cancelBtn.clicked.connect(self.worker.cancel)

        self.worker.totalComputed.connect(self.progress.setTotal, Qt.QueuedConnection)
        self.worker.progressChanged.connect(self.progress.setValue, Qt.QueuedConnection)
        self.worker.statusChanged.connect(self.progress.setLabelText, Qt.QueuedConnection)

        self.worker.moveToThread(self.thread)

        # Start
        self.thread.started.connect(self.worker.run)

        # Finish
        self.worker.error.connect(
            self.onSyncError, Qt.QueuedConnection
        )
        # worker end
        self.worker.finished.connect(self.thread.quit)

        # cleanup
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # ui end
        self.thread.finished.connect(
            self.onSyncFinished,
            Qt.QueuedConnection
        )
        self.thread.start()

    # =====================================================
    # CALLBACKS
    # =====================================================

    def onSyncFinished(self):
        #log("SYNC FINISHED CALLBACK")

        try:
            if self.progress:
                self.progress.close()
                self.progress.deleteLater()
                self.progress = None

            #log("SYNC FINISHED")

        except Exception:
            log(traceback.format_exc())

    def onSyncError(self, message):

        QMessageBox.critical(
            None,
            "Sync Error",
            message
        )

    # =====================================================
    # ACTIVE
    # =====================================================

    @err_catcher(name=__name__)
    def isActive(self):
        return True

class SyncProgressDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sync Media")
        self.setWindowFlags(
            Qt.Dialog |
            Qt.WindowTitleHint |
            Qt.CustomizeWindowHint
        )
        self.resize(450, 100)

        layout = QVBoxLayout(self)

        self.label = QLabel("Preparing sync...")
        layout.addWidget(self.label)

        self.bar = QProgressBar()
        self.bar.setMinimum(0)
        self.bar.setMaximum(0)  # indéterminé au départ
        self.bar.setValue(0)
        layout.addWidget(self.bar)

        self.cancelBtn = QPushButton("Cancel")
        layout.addWidget(self.cancelBtn)

    def setTotal(self, total):
        self.bar.setMaximum(total)
        self.bar.setValue(0)
        #log(f"TOTAL SET TO: {total}")

    def setValue(self, value):
        self.bar.setValue(value)

    def setLabelText(self, text):
        self.label.setText(text)