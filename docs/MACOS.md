# Setting Up Automated Pipelines with LaunchAgents on macOS

## Overview
This document describes the process of creating an automated pipeline using macOS LaunchAgents to run scripts on a schedule, along with common troubleshooting steps to address issues that might arise during setup.

## Creating a LaunchAgent Service

LaunchAgents are XML property list files (`plist`) that define services that run at specific intervals or under specific conditions in macOS. To set up a LaunchAgent:

1. Create a `.plist` file in `~/Library/LaunchAgents/` (for user-specific services)
2. Define the service configuration including the script to run and when to run it
3. Load the service with `launchctl`

### Sample LaunchAgent Configuration

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>com.example.run_word_addition_pipeline</string>
    
    <key>ProgramArguments</key>
    <array>
      <string>/bin/zsh</string>
      <string>-c</string>
      <string>/Users/username/Scripts/run_word_addition_pipeline.zsh</string>
    </array>
    
    <key>EnvironmentVariables</key>
    <dict>
      <key>PATH</key>
      <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
      <key>HOME</key>
      <string>/Users/username</string>
      <key>OPENAI_API_KEY</key>
      <string>sk-your-api-key-here</string>
    </dict>
    
    <key>StartCalendarInterval</key>
    <dict>
      <key>Hour</key>
      <integer>21</integer>
      <key>Minute</key>
      <integer>0</integer>
    </dict>
    
    <key>StandardOutPath</key>
    <string>/tmp/run_word_addition_pipeline.out</string>
    <key>StandardErrorPath</key>
    <string>/tmp/run_word_addition_pipeline.err</string>
  </dict>
</plist>
```

## Common Troubleshooting Steps

### 1. Use Absolute Paths
When working with LaunchAgents, always use full paths for:
- Script locations
- Python executable paths
- Any files your scripts need to read or write

```python
# Example of using full paths in Python scripts
PYTHON_PATH = "/Users/username/path/to/venv/bin/python"
subprocess.run([PYTHON_PATH, "/Users/username/path/to/script.py"])
```

### 2. Environment Variables
LaunchAgents run in a different environment than your terminal session. All required environment variables must be explicitly specified in the `plist` file:

- Include `PATH` to ensure commands can be found
- Set `HOME` to ensure proper user directory resolution
- Include any API keys or configuration variables your scripts need

### 3. API Key Formatting
When adding API keys or other sensitive strings to the `plist` file:

- Ensure there are no trailing newlines or spaces in the string
- Incorrect: `<string>sk-your-api-key\n</string>`
- Correct: `<string>sk-your-api-key</string>`

Newlines in API keys will cause authentication errors like:
```
Illegal header value b'Bearer sk-your-api-key\n'
```

### 4. Testing and Debugging

To manually test your LaunchAgent:
```bash
# Unload existing service
launchctl unload ~/Library/LaunchAgents/your-service.plist

# Load the service
launchctl load ~/Library/LaunchAgents/your-service.plist

# Trigger the service manually (doesn't respect calendar intervals)
launchctl start com.example.your-service

# Check output files
cat /tmp/your-service.out
cat /tmp/your-service.err
```

## Summary of Key Points

1. Always use full, absolute paths in LaunchAgent scripts
2. Explicitly define all required environment variables in the plist file
3. Ensure API keys and other strings don't have trailing whitespace or newlines
4. Use output and error log files for debugging
5. Test your service by manually triggering it with launchctl