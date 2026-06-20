# MDK 1.21.1 ModDevGradle Template

A production-ready NeoForge mod template for **Minecraft 1.21.1** using **ModDevGradle**.

This template starts from the standard MDK structure and adds modern development tooling, including GitHub Actions,
runtime testing, static analysis, automated releases, and dependency management.

---

## Features

- NeoForge + ModDevGradle for Minecraft **1.21.1**
- Kotlin DSL (build.gradle.kts) instead of Groovy for improved IDE support, type safety, and maintainability
- Java 21 toolchain
- Parchment mappings
- Multiple Gradle run configurations
    - Client
    - Secondary client
    - Dedicated server
    - GameTest server
    - Data generation
- Centralized mod metadata managed from Gradle
- Mixin and Access Transformer support
- GitHub Actions workflows
    - Build
    - Minecraft runtime testing
    - Qodana static analysis
    - Automated releases
- Dependabot configuration
- Optional CurseForge and Modrinth publishing

---

# Quick Start

## 1. Create a repository

Click **Use this template** on GitHub and clone your new repository.

```bash
git clone https://github.com/YOUR_NAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

---

## 2. Configure your mod

Edit the `ModConfig` object in `build.gradle.kts`.

```kotlin
object ModConfig {
    const val MOD_ID = "examplemod"
    const val MOD_NAME = "Example Mod"
    const val MOD_VERSION = "1.0.0"
    ...
}
```

At minimum, update:

- MOD_ID
- MOD_NAME
- MOD_VERSION
- MOD_GROUP_ID
- MOD_DISPLAY_URL
- MOD_AUTHORS
- MOD_DESCRIPTION

---

## 3. Rename the package

Move the example package:

```
src/main/java/io/github/mochi_753/examplemod
```

to your own package.

Also rename:

```
src/main/resources/examplemod.mixins.json
```

to match your new mod ID.

---

## 4. Build

Linux/macOS

```bash
./gradlew build
```

Windows

```bat
gradlew.bat build
```

The compiled JAR will be generated in

```
build/libs
```

---

# Requirements

- Java 21 or newer
- Git

For CI workflows:

- GitHub repository

GitHub Actions currently builds with **Temurin JDK 25** while Minecraft runtime tests use **Java 21**.

---

# Gradle Tasks

| Task                | Description                                       |
|---------------------|---------------------------------------------------|
| `runClient`         | Launch Minecraft client                           |
| `runClient2`        | Launch a secondary client for multiplayer testing |
| `runServer`         | Launch dedicated server (`--nogui`)               |
| `runGameTestServer` | Launch GameTest server                            |
| `runData`           | Generate data into `src/generated/resources`      |
| `build`             | Build the mod                                     |

---

# Mod Metadata

Most project information is stored in a single place:

```
build.gradle.kts
```

The `generateModMetadata` task generates

```
src/main/templates/META-INF/neoforge.mods.toml
```

automatically, keeping metadata synchronized with Gradle configuration.

---

# GitHub Actions

This template includes four workflows.

| Workflow               | Purpose                                         |
|------------------------|-------------------------------------------------|
| Build                  | Compile the project and upload artifacts        |
| Minecraft Runtime Test | Verify the built mod loads in Minecraft         |
| Qodana                 | Static code analysis                            |
| Release                | Publish GitHub / CurseForge / Modrinth releases |

---

## Build

Runs on:

- Push
- Pull Request
- Manual dispatch

Steps:

1. Checkout
2. Setup Java
3. Build
4. Upload artifacts

---

## Minecraft Runtime Test

Runs on:

- Pull Requests to `main`
- Manual dispatch

The workflow:

- builds the mod
- stages the built JAR
- launches a headless Minecraft client
- launches a headless Minecraft server

This verifies that the mod can actually load, not just compile.

---

## Qodana

Runs JetBrains Qodana static analysis.

To enable pull request integration, add:

```
QODANA_TOKEN
```

as a repository secret.

---

## Release

Supports:

- Release
- Beta
- Alpha

Optional publishing targets:

- GitHub Releases
- CurseForge
- Modrinth

The workflow automatically:

- builds the project
- generates changelogs with `git-cliff`
- creates version tags
- generates artifact attestations
- publishes releases

---

# Publishing

Set your project IDs inside `ModConfig` in `build.gradle.kts`.

```kotlin
const val CURSEFORGE_PROJECT_ID = "..."
const val MODRINTH_PROJECT_ID = "..."
```

Repository secrets:

| Secret             | Purpose               |
|--------------------|-----------------------|
| `CURSEFORGE_TOKEN` | CurseForge publishing |
| `MODRINTH_TOKEN`   | Modrinth publishing   |

### Configuring Dependencies

The release scripts read dependency information from:

* `src/main/python/dependencies.curseforge.json`
* `src/main/python/dependencies.modrinth.json`

If your mod has no dependencies, leave the files as an empty JSON array:

```json
[]
```

Otherwise, add your project's dependencies using the appropriate format for each platform.

Example (`dependencies.curseforge.json`):

```json
[
  {
    "slug": "jei", // The slug of the project it depends on.
    "projectID": 238222, // The ID of the project being depended on. Must be a number.
    "type": "requiredDependency" // Dependency type. You can select one of the following: [“embeddedLibrary”, “incompatible”, “optionalDependency”, ‘requiredDependency’, “tool”].
  }
]
```

Example (`dependencies.modrinth.json`):

```json
[
  {
    "version_id": null, // The ID of the version being used. If this is null, it means any version can be used.
    "project_id": "u6dRKJwZ", // The ID of the project being depended on.
    "file_name": null, // I think that's the filename within the dependent project. I'm sorry, I'm not really sure.
    "dependency_type": "required" // Dependency type. You can select one of the following: [“required”, “optional”, “incompatible”, ‘embedded’].
  }
]
```

Replace the example values with the dependencies required by your own mod before publishing.

---

# Dependabot

Weekly updates for:

- Gradle
- GitHub Actions

---

# Repository Layout

```text
.
├── .github/
├── build.gradle.kts
├── gradle.properties
├── settings.gradle.kts
├── src/
│   └── main/
│       ├── java/
│       ├── python/
│       ├── resources/
│       └── templates/
└── README.md
```

---

# Custom Dependencies

Commented examples for CurseForge Maven and Modrinth Maven repositories are already included in `build.gradle.kts`.

Uncomment and configure them if required by your project.

---

# License

This template contains both:

- LICENSE.txt
- TEMPLATE_LICENSE.txt

Update them as appropriate for your own project.

The author of this template does not require mods created using this template to be released under any particular license. You are free to choose the license for your own mod.
