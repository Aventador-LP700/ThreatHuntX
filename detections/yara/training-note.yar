rule ThreatHuntX_Training_Note
{
    meta:
        description = "Classifies the bundled ThreatHuntX case note"
        scope = "Educational text samples"

    strings:
        $header = "THREATHUNTX FORENSICS PRACTICE" ascii
        $case = "TRAINING CASE THX-09" ascii

    condition:
        filesize < 4096 and all of them
}
