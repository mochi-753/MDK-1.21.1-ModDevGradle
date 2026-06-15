# MDK 1.21.1 ModDevGradle

A developer-ready NeoForge MDK template for Minecraft 1.21.1 using Gradle Kotlin DSL and the NeoForge ModDevGradle plugin. The repository is intentionally small: replace the example mod metadata, add your Java sources, then use the provided Gradle runs and release helper scripts to build, test, generate data, and publish your mod.

## Features

- **Minecraft 1.21.1 + NeoForge setup**: preconfigured for NeoForge `21.1.233`, Minecraft `1.21.1`, Java 21, and Parchment mappings.
- **Centralized mod configuration**: mod id, name, version, license, authors, display URL, and description are defined in one Kotlin object and expanded into mod metadata at build time.
- **IDE-friendly ModDevGradle runs**: ready-made client, server, game test server, and data generation run configurations.
- **Generated mod metadata**: `neoforge.mods.toml` is templated from `src/main/templates` so metadata stays in sync with Gradle constants.
- **Generated resources support**: `src/generated/resources` is wired into the main resource set for data generators.
- **Local runtime dependency bucket**: a `localRuntime` configuration is available for dependencies needed only while launching local dev runs.
- **Java 21 toolchain resolution**: Gradle is configured to use the Adoptium Java 21 toolchain and Foojay toolchain resolver.
- **Gradle performance defaults**: daemon, parallel execution, build cache, and configuration cache are enabled.
- **IDE source and Javadoc downloads**: IntelliJ IDEA module settings request downloaded sources and Javadocs.
- **Modrinth and CurseForge release helpers**: Python scripts upload built jars and dependency metadata to Modrinth or CurseForge.
- **MIT licensing files**: includes the repository license and the NeoForge template license.

## Requirements

- Git.
- Java 21. You can install it yourself, or let Gradle resolve an Adoptium toolchain through the configured Foojay resolver.
- An IDE that supports Gradle projects, such as IntelliJ IDEA.
- Python 3 and the packages in `src/main/python/requirements.txt` only if you use the release upload scripts.

## Quick start

1. Clone this repository.
2. Import the project as a Gradle project in your IDE.
3. Run an initial Gradle sync or execute:

   ```bash
   ./gradlew tasks
   ```

4. Update the template values in `build.gradle.kts` under `ModConfig`.
5. Update the Java package and `MOD_ID` in `src/main/java/io/github/mochi_753/examplemod/ExampleMod.java`.
6. Build the mod:

   ```bash
   ./gradlew build
   ```

The distributable jar is created under `build/libs`.

## Project layout

```text
.
├── build.gradle.kts                         # Main Gradle build and ModDevGradle configuration
├── gradle.properties                        # Gradle JVM/performance/configuration-cache defaults
├── settings.gradle.kts                      # Plugin repositories and Java toolchain resolver
├── src/main/java/.../ExampleMod.java        # Example NeoForge @Mod entrypoint
├── src/main/templates/META-INF/neoforge.mods.toml
│                                             # Metadata template expanded by Gradle
├── src/main/python/                         # Modrinth/CurseForge release helper scripts
├── LICENSE.txt                              # License for this template repository
└── TEMPLATE_LICENSE.txt                     # License for the original NeoForge MDK template files
```

## Feature details and how to enable them

### 1. Minecraft, NeoForge, and mappings configuration

The template targets:

- Minecraft: `1.21.1`
- NeoForge: `21.1.233`
- Parchment mappings: `2024.11.17`
- Java: `21`

These values are defined in `ModConfig` inside `build.gradle.kts`.

**How to enable or customize**

No extra setup is required. To change versions, edit these constants:

```kotlin
const val MINECRAFT_VERSION = "1.21.1"
const val MINECRAFT_VERSION_RANGE = "[1.21.1]"
const val NEO_VERSION = "21.1.233"
const val NEO_VERSION_RANGE = "[21.1,)"
const val PARCHMENT_MAPPING_VERSION = "2024.11.17"
```

After changing versions, refresh Gradle in your IDE and run:

```bash
./gradlew build
```

### 2. Centralized mod metadata

The following values are centralized in `ModConfig`:

- `MOD_ID`
- `MOD_NAME`
- `MOD_LICENSE`
- `MOD_VERSION`
- `MOD_GROUP_ID`
- `MOD_DISPLAY_URL`
- `MOD_AUTHORS`
- `MOD_DESCRIPTION`

Gradle uses these constants for the project version/group, archive name, NeoForge mod registration, and generated `neoforge.mods.toml` metadata.

**How to enable or customize**

Edit the `ModConfig` constants in `build.gradle.kts`. At minimum, change:

```kotlin
const val MOD_ID = "examplemod"
const val MOD_NAME = "Example Mod"
const val MOD_VERSION = "1.0.0"
const val MOD_GROUP_ID = "io.github.mochi_753.examplemod"
const val MOD_AUTHORS = "Mochi753"
const val MOD_DESCRIPTION = "EXAMPLE MOD"
```

Then update the Java mod id constant to match:

```java
public static final String MOD_ID = "examplemod";
```

Your `MOD_ID` must also match the mod id used by generated data, game tests, and dependency declarations.

### 3. NeoForge mod entrypoint

`ExampleMod.java` provides a minimal NeoForge entrypoint annotated with `@Mod`. It receives the mod event bus and mod container in its constructor.

**How to enable or customize**

Rename the package and class for your mod, then register content from the constructor. For example, after creating deferred registers, call their `register(eventBus)` methods inside the constructor.

If you rename the package, also move the file to the matching directory under `src/main/java`.

### 4. Client run configuration

The `client` run launches Minecraft in a local development client using `runs/client` as its game directory. It enables game test namespaces for the configured mod id and sets registry logging markers.

**How to enable or run**

From a terminal:

```bash
./gradlew runClient
```

From IntelliJ IDEA, import/sync the Gradle project and use the generated NeoForge client run configuration.

### 5. Server run configuration

The `server` run launches a dedicated NeoForge server with `--nogui` using `runs/server` as its game directory.

**How to enable or run**

```bash
./gradlew runServer
```

Use this to test server-side behavior, networking, data sync, and dedicated-server compatibility.

### 6. Game test server run configuration

The `gameTestServer` run is configured with NeoForge's `gameTestServer` type and the same game test namespace as the mod id.

**How to enable or run**

```bash
./gradlew runGameTestServer
```

Add your game tests under your mod's Java sources, ensure their namespace matches `ModConfig.MOD_ID`, and run the task above.

### 7. Data generation run configuration

The `data` run invokes NeoForge data generation with:

- `--mod <MOD_ID>`
- `--all`
- output directory: `src/generated/resources`
- existing resources: `src/main/resources`

**How to enable or run**

```bash
./gradlew runData
```

Generated files are written to `src/generated/resources`, which is already included in the main resources source set. Commit generated assets/data that should be part of your mod release.

### 8. Generated mod metadata

`src/main/templates/META-INF/neoforge.mods.toml` contains placeholders such as `${mod_id}`, `${mod_version}`, and `${minecraft_version_range}`. The `generateModMetadata` Gradle task expands those placeholders into `build/generated/sources/modMetadata`.

**How to enable or customize**

This is enabled automatically. To change metadata fields, either:

1. edit values in `ModConfig`, or
2. add new placeholders to `generateModMetadata` and reference them in `src/main/templates/META-INF/neoforge.mods.toml`.

The generated metadata task is also registered with NeoForge IDE sync.

### 9. Optional mixins and access transformers

The metadata template includes commented examples for mixins and access transformers:

```toml
#[[mixins]]
#config="${mod_id}.mixins.json"

#[[accessTransformers]]
#file="META-INF/accesstransformer.cfg"
```

**How to enable mixins**

1. Uncomment the `[[mixins]]` block in `src/main/templates/META-INF/neoforge.mods.toml`.
2. Add your mixin config file to resources, for example `src/main/resources/examplemod.mixins.json`.
3. Add your mixin classes under `src/main/java`.
4. Refresh Gradle and test with `./gradlew runClient` or `./gradlew runServer`.

**How to enable access transformers**

1. Uncomment the `[[accessTransformers]]` block.
2. Add `src/main/resources/META-INF/accesstransformer.cfg`.
3. Define the access transformations you need.
4. Rebuild with `./gradlew build`.

### 10. Dependencies

The build currently declares no mod or library dependencies beyond the configured NeoForge environment. `mavenCentral()` is available for normal Java libraries.

**How to enable compile/runtime dependencies**

Add dependencies to the `dependencies` block in `build.gradle.kts`.

For normal libraries:

```kotlin
dependencies {
    implementation("group:artifact:version")
}
```

For dependencies used only when running locally, use the provided `localRuntime` configuration:

```kotlin
dependencies {
    localRuntime("group:artifact:version")
}
```

If you need dependencies from another Maven repository, add that repository to the `repositories` block.

### 11. Resource generation support

The main resource set includes `src/generated/resources`, while cache folders under generated resources are excluded.

**How to enable or use**

Run:

```bash
./gradlew runData
```

Then review and commit the generated files you want to ship.

### 12. Java toolchain and IDE configuration

The build requests Java 21 from the Adoptium vendor. `settings.gradle.kts` applies Foojay's toolchain resolver plugin, allowing Gradle to find or download matching JDKs when needed. IntelliJ IDEA source and Javadoc downloads are enabled.

**How to enable or use**

This is enabled automatically. If your IDE prompts for a Gradle JVM, choose Java 21 or allow Gradle toolchains to provision one. After import, refresh Gradle to generate run configurations and download sources.

### 13. Gradle performance settings

`gradle.properties` enables:

- Gradle daemon
- parallel execution
- build cache
- configuration cache
- Kotlin DSL warnings as errors
- `-Xmx1G` Gradle JVM memory

**How to enable or customize**

These settings are active automatically. If a plugin or custom task is not compatible with configuration cache, temporarily disable it with:

```bash
./gradlew build --no-configuration-cache
```

Or edit `gradle.properties` if you want a permanent change.

### 14. Modrinth release helper

`src/main/python/release.modrinth.py` uploads every `*.jar` in the current working directory to Modrinth. It reads:

- changelog text from `CHANGELOG.md`
- dependency metadata from `src/main/python/dependencies.modrinth.json`
- project and authentication data from environment variables

Required environment variables:

- `REPOSITORY_NAME`
- `VERSION`
- `MODRINTH_PROJECT_ID`
- `MODRINTH_TOKEN`
- `REPOSITORY`

**How to enable or run**

1. Install Python dependencies:

   ```bash
   python -m pip install -r src/main/python/requirements.txt
   ```

2. Build your mod:

   ```bash
   ./gradlew build
   ```

3. Copy or run the script from a directory containing the jar you want to upload.
4. Set the required environment variables.
5. Run:

   ```bash
   python src/main/python/release.modrinth.py
   ```

6. Edit `src/main/python/dependencies.modrinth.json` to declare Modrinth dependencies. The included example declares JEI as a required dependency by project id.

### 15. CurseForge release helper

`src/main/python/release.curseforge.py` uploads every `*.jar` in the current working directory to CurseForge. It converts `CHANGELOG.md` from Markdown to HTML and reads dependency relations from `src/main/python/dependencies.curseforge.json`.

Required environment variables:

- `REPOSITORY_NAME`
- `VERSION`
- `CURSEFORGE_PROJECT_ID`
- `CURSEFORGE_TOKEN`
- `REPOSITORY`

**How to enable or run**

1. Install Python dependencies:

   ```bash
   python -m pip install -r src/main/python/requirements.txt
   ```

2. Build your mod:

   ```bash
   ./gradlew build
   ```

3. Copy or run the script from a directory containing the jar you want to upload.
4. Set the required environment variables.
5. Run:

   ```bash
   python src/main/python/release.curseforge.py
   ```

6. Edit `src/main/python/dependencies.curseforge.json` to declare CurseForge dependency relations. The included example declares JEI as a required dependency.

## Common Gradle commands

| Command | Purpose |
| --- | --- |
| `./gradlew build` | Compile, process resources, and create the mod jar. |
| `./gradlew runClient` | Launch the development Minecraft client. |
| `./gradlew runServer` | Launch the dedicated development server. |
| `./gradlew runGameTestServer` | Run the NeoForge game test server. |
| `./gradlew runData` | Generate data into `src/generated/resources`. |
| `./gradlew clean` | Remove Gradle build outputs. |
| `./gradlew --refresh-dependencies` | Force Gradle to resolve dependencies again. |

## Turning this template into your own mod

Use this checklist when starting a new mod from the template:

1. Replace all `ModConfig` values in `build.gradle.kts`.
2. Rename the Java package and `ExampleMod` class.
3. Make sure the Java `MOD_ID` equals `ModConfig.MOD_ID`.
4. Update `LICENSE.txt` if your project uses a different license.
5. Update or remove `TEMPLATE_LICENSE.txt` only if you understand the template license requirements.
6. Add your registrations, content, assets, data, and optional generated resources.
7. Add dependencies to `build.gradle.kts` and to the Modrinth/CurseForge dependency JSON files if those dependencies are required for published releases.
8. Run `./gradlew runClient`, `./gradlew runServer`, and `./gradlew build` before publishing.

## License

This repository is licensed under the MIT License. The original NeoForge MDK template files are also covered by the MIT template license included in `TEMPLATE_LICENSE.txt`.
