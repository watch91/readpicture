# 获取脚本所在的文件夹路径
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 要添加的路径（就是当前文件夹）
$pathToAdd = $scriptDir

# 选择添加到“用户变量”还是“系统变量”
# 推荐使用 'User'（无需管理员权限），如果选 'Machine' 需要右键“以管理员身份运行”
$targetScope = 'User'  # 或 'Machine'

# 获取当前 PATH
$currentPath = [Environment]::GetEnvironmentVariable('Path', $targetScope)

# 检查路径是否已存在（忽略大小写）
if ($currentPath -split ';' -contains $pathToAdd) {
    Write-Host "?


 路径已存在于 $targetScope PATH 中：$pathToAdd" -ForegroundColor Green
} else {
    # 追加新路径
    $newPath = $currentPath.TrimEnd(';') + ';' + $pathToAdd
    [Environment]::SetEnvironmentVariable('Path', $newPath, $targetScope)
    Write-Host "? 成功将路径添加到 $targetScope PATH：$pathToAdd" -ForegroundColor Green
}

# 刷新当前 PowerShell 会话的环境变量（无需重启）
$env:Path = [Environment]::GetEnvironmentVariable('Path', 'User') + ';' + [Environment]::GetEnvironmentVariable('Path', 'Machine')

Write-Host "设置完成！请重新打开 CMD 窗口，即可使用 'readpicture' 命令。" -ForegroundColor Yellow