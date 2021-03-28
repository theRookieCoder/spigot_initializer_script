import os

GREEN = "\033[92m"
CYAN = "\033[96m"
RED = "\033[31m"
END = "\033[0m"
ITALIC = "\x1B[3m"

pluginName = ""
groupId = ""
path = ""
version = "1.16.5"

welcome = f"{CYAN}Welcome to Bukkit (Spigot) plugin wizard!{END}" + r"""
     __/\__
  _  \\''//
-( )-/_()_\   
 .'.  | . \
  |   | .  \
 .'.  \_____'.
Created by theRookieCoder
"""

print(welcome)
pluginName = input(f"{GREEN}? {CYAN}What would you like the name of your plugin to be {END}")
groupId = input(f"{GREEN}? {CYAN}What is your group ID (e.g. io.github.therookicoder) {END}")
if len(groupId.split('.')) != 3:
  print(f"{RED}GroupIDError: GroupID '{groupId}' does not contain three objects{END}")
  exit()
path = input(f"{GREEN}? {CYAN}Where would you like your project to be (e.g /Users/name/IdeaProjects) {END}")
if not os.path.exists(path):
  print(f"{RED}FileError: Path '{path}' does not exist{END}")
  exit()

try:
  os.mkdir(f"{path}/{pluginName}")
except FileExistsError:
  print(f"{RED}FileError: Project {pluginName} alreasy exists in {path}{END}")
  exit()

os.makedirs(f"{path}/{pluginName}/server", exist_ok=True)
os.makedirs(f"{path}/{pluginName}/.idea", exist_ok=True)
os.makedirs(f"{path}/{pluginName}/src/main/java/{groupId.split('.')[0]}/{groupId.split('.')[1]}/{groupId.split('.')[2]}/{pluginName.lower()}", exist_ok=True)
os.makedirs(f"{path}/{pluginName}/src/main/resources/", exist_ok=True)
main = open(f"{path}/{pluginName}/src/main/java/{groupId.split('.')[0]}/{groupId.split('.')[1]}/{groupId.split('.')[2]}/{pluginName.lower()}/{pluginName}.java", "x")
eula = open(f"{path}/{pluginName}/server/eula.txt", "x")
yml = open(f"{path}/{pluginName}/src/main/resources/plugin.yml", "x")
pom = open(f"{path}/{pluginName}/pom.xml", "x")
run = open(f"{path}/{pluginName}/.idea/Build_and_run.xml", "x")
print("Downloading server...", end=" ", flush=True)
os.system(f"wget https://papermc.io/api/v1/paper/{version}/latest/download -o {path}/{pluginName}/server/server.jar &> /dev/null")
print("✓")

if input(f"{GREEN}? {CYAN}Do you agree to the Mojang's EULA? (https://account.mojang.com/documents/minecraft_eula) y/n {END}") == "y":
  eula.write("eula = true")
else:
  print(f"{RED}Warning: To run the Paper server for testing/using the plugin, you have to agree to Mojang's EULA{END}")
eula.close()

main.write(f"""package {groupId}.{pluginName.lower()}

import org.bukkit.java.JavaPlugin;

public final class {pluginName} extends JavaPlugin {{
  @Override
  public void onEnable() {{
    // Code to be run at the plugin's initialization
  }}

  @Override
  public void onDisable() {{
    // Code to be run before the plugin is disabled
  }}
}}
""")
main.close()

yml.write(f"""name: #TODO: Enter name here
main: {groupId}.{pluginName.lower}.{pluginName}
version: 0.0.1
description: #TODO: Enter description here
api-version: {version[0:3]}
author: #TODO: Enter your name/alias here
""")
yml.close()

pom.write(f"""<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>
    <build>
      <plugins>
          <plugin>
              <version>3.8.1</version>
              <groupId>org.apache.maven.plugins</groupId>
              <artifactId>maven-compiler-plugin</artifactId>
              <configuration>
                  <source>1.8</source>
                  <target>1.8</target>
              </configuration>
          </plugin>
      </plugins>
      <directory>server/plugins</directory>
   </build>
  <modelVersion>4.0.0</modelVersion>
  <groupId>{groupId}</groupId>
  <artifactId>{pluginName}</artifactId>
    <!-- Increment the below value when changes are made -->
  <version>0.0.1-SNAPSHOT</version>
  <repositories>
      <repository>
          <id>spigot-repo</id>
          <url>https://hub.spigotmc.org/nexus/content/repositories/snapshots/</url>
      </repository>
   </repositories>
   <dependencies>
       <dependency>
           <groupId>org.spigotmc</groupId>
           <artifactId>spigot-api</artifactId>
           <version>{version}-R0.1-SNAPSHOT</version>
           <scope>provided</scope>
       </dependency>
   </dependencies>
</project>
""")

run.write("""<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="Build and run" type="JarApplication">
    <option name="JAR_PATH" value="$PROJECT_DIR$/server/server.jar" />
    <option name="VM_PARAMETERS" value="-Xmx2G" />
    <option name="PROGRAM_PARAMETERS" value="nogui" />
    <option name="WORKING_DIRECTORY" value="$PROJECT_DIR$/server" />
    <option name="ALTERNATIVE_JRE_PATH_ENABLED" value="true" />
    <option name="ALTERNATIVE_JRE_PATH" value="15" />
    <module name="TestPlugin" />
    <method v="2">
      <option name="Maven.BeforeRunTask" enabled="true" file="$PROJECT_DIR$/pom.xml" goal="package -Ddir=&quot;$PROJECT_DIR$/server/plugins&quot;" />
    </method>
  </configuration>
</component>
""")

print(f"""
{CYAN}Plugin name:        {END}{pluginName}
{CYAN}Group ID:           {END}{groupId}
{CYAN}Minecraft Version:  {END}{version}
{CYAN}Project Location:   {END}{path}/{pluginName}
{CYAN}Java build version: {END}1.8

YOUR TODO:
- Agree to Mojang's eula to run the server if you haven't yet
- In the plugin.yml file:
  - Enter your plugin's {ITALIC}display{END} name under 'name: '
  - Enter a description of your plugin under 'description: '
  - Enter your name/alias under 'author: '
- Open the project in Eclipse/Intellij IDEA to download the Spigot API
- Implement onEnable and onDisable functions {ITALIC}if required{END}
- If you're using Intellij IDEA: 
  - Try running the 'Build and run' run config and see if it works
""")
