param($CommitMsgFile)

$msg = Get-Content $CommitMsgFile -Raw
$firstLine = ($msg -split "`n")[0]

if ($firstLine.Length -gt 60) {
    Write-Error "Error: First line of commit message must be ≤60 characters."
    exit 1
}

if ($firstLine -ne $firstLine.ToLower()) {
    Write-Error "Error: First line of commit message must be lowercase."
    exit 1
}

$types = @('feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore', 'perf', 'ci', 'build', 'revert')
$valid = $false
foreach ($type in $types) {
    if ($firstLine -match "^$type:\s") {
        $valid = $true
        break
    }
}

if (-not $valid) {
    Write-Error "Error: Commit message must start with a conventional commit type followed by a space."
    exit 1
}

exit 0