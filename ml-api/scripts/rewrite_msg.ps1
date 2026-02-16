$msg = $input
$lines = $msg -split "`n"
$firstLine = $lines[0].ToLower()
if ($firstLine.Length -gt 60) {
    $firstLine = $firstLine.Substring(0,60)
}
$lines[0] = $firstLine
$lines -join "`n"