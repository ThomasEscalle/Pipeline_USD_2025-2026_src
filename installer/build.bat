@echo off
setlocal

echo ========================================
echo Script de build pour BadgerInstaller
echo ========================================

:: Définir le dossier de build
set BUILD_DIR=build

:: Vérifier si le dossier build existe
if exist "%BUILD_DIR%" (
    echo Le dossier build existe deja.
) else (
    echo Creation du dossier build...
    mkdir "%BUILD_DIR%"
    if errorlevel 1 (
        echo ERREUR: Impossible de creer le dossier build
        pause
        exit /b 1
    )
    echo Dossier build cree avec succes.
)

:: Aller dans le dossier build
echo Navigation vers le dossier build...
cd "%BUILD_DIR%"
if errorlevel 1 (
    echo ERREUR: Impossible d'acceder au dossier build
    pause
    exit /b 1
)

:: Exécuter cmake pour générer le projet
echo ========================================
echo Generation du projet avec CMake...
echo ========================================
cmake ../src
if errorlevel 1 (
    echo ERREUR: Echec de la generation CMake
    echo Verifiez que CMake est installe et accessible dans PATH
    pause
    exit /b 1
)

echo ========================================
echo Generation CMake terminee avec succes!
echo ========================================

:: Vérifier si le fichier .sln existe
if exist "BadgerInstaller.sln" (
    echo Ouverture de BadgerInstaller.sln...
    start "" "BadgerInstaller.sln"
    echo Solution Visual Studio ouverte.
) else (
    echo ATTENTION: BadgerInstaller.sln n'a pas ete trouve.
    echo Verification des fichiers generes...
    dir *.sln
)

echo ========================================
echo Script de build termine!
echo ========================================
pause
