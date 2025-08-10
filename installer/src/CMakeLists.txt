# CMakeLists.txt pour BadgerInstaller
cmake_minimum_required(VERSION 3.15)

# Nom du projet
project(BadgerInstaller VERSION 1.0.0 LANGUAGES CXX)

# Configuration C++
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Configuration des dossiers de sortie
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Définir les dossiers source et destination
set(SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR})
set(BIN_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../bin)

# Rechercher récursivement tous les fichiers .cpp et .h
file(GLOB_RECURSE SOURCES 
    "${SOURCE_DIR}/*.cpp"
    "${SOURCE_DIR}/*.cxx"
    "${SOURCE_DIR}/*.cc"
)

file(GLOB_RECURSE HEADERS 
    "${SOURCE_DIR}/*.h"
    "${SOURCE_DIR}/*.hpp"
    "${SOURCE_DIR}/*.hxx"
)

# Afficher les fichiers trouvés (pour débogage)
message(STATUS "Fichiers sources trouvés:")
foreach(SOURCE_FILE ${SOURCES})
    message(STATUS "  ${SOURCE_FILE}")
endforeach()

message(STATUS "Fichiers headers trouvés:")
foreach(HEADER_FILE ${HEADERS})
    message(STATUS "  ${HEADER_FILE}")
endforeach()

# Créer l'exécutable si des sources sont trouvées
if(SOURCES)
    # Créer l'exécutable BadgerInstaller
    add_executable(BadgerInstaller ${SOURCES} ${HEADERS})
    
    # Définir le nom de sortie explicitement
    set_target_properties(BadgerInstaller PROPERTIES
        OUTPUT_NAME "BadgerInstaller"
        SUFFIX ".exe"
    )
    
    # Inclure les dossiers contenant les headers
    target_include_directories(BadgerInstaller PRIVATE ${SOURCE_DIR})
    
    # Rechercher et inclure tous les sous-dossiers contenant des headers
    file(GLOB_RECURSE HEADER_DIRS LIST_DIRECTORIES true "${SOURCE_DIR}/*")
    foreach(HEADER_DIR ${HEADER_DIRS})
        if(IS_DIRECTORY ${HEADER_DIR})
            target_include_directories(BadgerInstaller PRIVATE ${HEADER_DIR})
        endif()
    endforeach()
    
    # Configuration spécifique à Windows
    if(WIN32)
        # Ajouter les définitions Windows
        target_compile_definitions(BadgerInstaller PRIVATE 
            WIN32_LEAN_AND_MEAN
            NOMINMAX
            _CRT_SECURE_NO_WARNINGS
        )
        
        # Configuration pour Release/Debug
        target_compile_options(BadgerInstaller PRIVATE
            $<$<CONFIG:Debug>:/Od /Zi>
            $<$<CONFIG:Release>:/O2>
        )
    endif()
    
    # Commande personnalisée pour copier l'exécutable vers le dossier bin après compilation
    add_custom_command(TARGET BadgerInstaller POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E make_directory ${BIN_DIR}
        COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:BadgerInstaller> ${BIN_DIR}/
        COMMENT "Copie de BadgerInstaller.exe vers le dossier bin"
    )
    
    # Afficher le message de succès
    message(STATUS "Configuration terminée pour BadgerInstaller.exe")
    message(STATUS "L'exécutable sera copié dans: ${BIN_DIR}")
    
else()
    message(WARNING "Aucun fichier source (.cpp, .cxx, .cc) trouvé dans ${SOURCE_DIR}")
    message(STATUS "Veuillez ajouter des fichiers source C++ pour compiler l'exécutable")
endif()

# Configuration pour les builds
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    message(STATUS "Configuration: Debug")
elseif(CMAKE_BUILD_TYPE STREQUAL "Release")
    message(STATUS "Configuration: Release")
else()
    set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Build type" FORCE)
    message(STATUS "Configuration par défaut: Release")
endif()

# Afficher les informations de configuration
message(STATUS "========================================")
message(STATUS "Projet: ${PROJECT_NAME}")
message(STATUS "Version: ${PROJECT_VERSION}")
message(STATUS "Standard C++: ${CMAKE_CXX_STANDARD}")
message(STATUS "Dossier source: ${SOURCE_DIR}")
message(STATUS "Dossier de destination: ${BIN_DIR}")
message(STATUS "========================================")