$csvPath = "labels.csv"

function updateCSV {
    param (
        [string]$folderName,
        [string]$fileName
    )

    Write-Host "Processing file $fileName in folder $folderName"

    try {
        # Check if the CSV file exists, if not, create it with headers
        if (-not (Test-Path $csvPath)) {
            Write-Host "Creating new CSV file with headers"
            $headers = @("filename", "obstacle_forward", "path_straight", "steps")  # Add other labels as needed
            $headers -join ',' | Out-File -FilePath $csvPath -Encoding UTF8
        }

        # Load existing CSV data into an array list
        $csvData = Import-Csv -Path $csvPath

        # Convert CSV data to ArrayList
        $csvData = [System.Collections.ArrayList]@($csvData)

        # Find the entry for the current file
        $entry = $csvData | Where-Object { $_.filename -eq $fileName }

        if ($entry) {
            # Update existing entry with the folderName
            Write-Host "Updating existing entry for $fileName"
            $entry.$folderName = "1"
        } else {
            Write-Host "Adding new entry for $fileName"
            $newEntry = @{
                "filename"         = $fileName
                "obstacle_forward" = "0"
                "path_straight"    = "0"
                "steps" = "0"
            }

            # Add the folder name column with value "1"
            if ($newEntry.ContainsKey($folderName)) {
                $newEntry[$folderName] = "1"
            } else {
                Write-Host "Warning: The folder name '$folderName' is not a recognized label."
                $newEntry.Add($folderName, "1")
            }

            # Convert hashtable to PSObject and add to CSV data
            $newRow = New-Object PSObject -Property $newEntry
            [void]$csvData.Add($newRow)

            Write-Host "New entry added: $($newRow | ConvertTo-Json)"
        }

        # Ensure the correct order of headers when exporting to CSV
        $csvData | Select-Object -Property "filename", "obstacle_forward", "path_straight", "steps" | Export-Csv -Path $csvPath -NoTypeInformation
    } catch {
        Write-Host "Error processing file name $fileName and folder name $folderName : $_"
    }
}

Get-ChildItem -Path "val" -Recurse | ForEach-Object {
    if ($_.PSIsContainer) {
        $files = Get-ChildItem -Path $_.FullName | Where-Object { -not $_.PSIsContainer }
        if ($files) {
            foreach ($file in $files) {
                updateCSV -folderName $_.Name -fileName $file.Name
            }
        }
    }
}

Get-ChildItem -Path "train" -Recurse | ForEach-Object {
    if ($_.PSIsContainer) {
        $files = Get-ChildItem -Path $_.FullName | Where-Object { -not $_.PSIsContainer }
        if ($files) {
            foreach ($file in $files) {
                updateCSV -folderName $_.Name -fileName $file.Name
            }
        }
    }
}

Write-Host -NoNewLine 'Press any key to continue...'
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
