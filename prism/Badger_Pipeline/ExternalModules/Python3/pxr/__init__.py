__all__ = ['Tf', 'Gf', 'Trace', 'Work', 'Plug', 'Vt', 'Ts', 'Ar', 'Kind', 'Sdf', 'Ndr', 'Sdr', 'Pcp', 'Usd', 'UsdGeom', 'UsdVol', 'UsdMedia', 'UsdShade', 'UsdLux', 'UsdProc', 'UsdRender', 'UsdHydra', 'UsdRi', 'UsdSemantics', 'UsdSkel', 'UsdUI', 'UsdUtils', 'UsdPhysics', 'UsdValidation']


# appended to this file for the windows PyPI package
import os, sys
dllPath = os.path.split(os.path.realpath(__file__))[0]
if sys.version_info >= (3, 8, 0):
    os.environ['PXR_USD_WINDOWS_DLL_PATH'] = dllPath
# Note that we ALWAYS modify the PATH, even for python-3.8+. This is because:
#    - Anaconda python interpreters are modified to use the old, pre-3.8, PATH-
#      based method of loading dlls
#    - extra calls to os.add_dll_directory won't hurt these anaconda
#      interpreters
#    - similarly, adding the extra PATH entry shouldn't hurt standard python
#      interpreters
#    - there's no canonical/bulletproof way to check for an anaconda interpreter
os.environ['PATH'] = dllPath + os.pathsep + os.environ['PATH']
