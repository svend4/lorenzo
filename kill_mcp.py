import subprocess, sys

result = subprocess.run(
    ['powershell', '-Command',
     'Get-Process python -ErrorAction SilentlyContinue | '
     'ForEach-Object { '
     '  $cmd = (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)").CommandLine; '
     '  if ($cmd -like "*mcp*server*") { '
     '    Write-Output "$($_.Id) $cmd"; '
     '    Stop-Process -Id $_.Id -Force '
     '  } '
     '}'],
    capture_output=True, text=True
)
output = result.stdout.strip()
if output:
    for line in output.splitlines():
        print(f'Killed: {line[:100]}')
else:
    print('No MCP server processes found (or already restarted)')
print('Done.')
