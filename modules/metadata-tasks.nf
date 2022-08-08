
process GET_GSE_REPORT {
        
    input:
    val GSE

    output:
    path "*.xml"

	script: 
/// sleep ${GSE[-1]} introduces a random delay in the download of the files.
	"""
    sleep ${GSE[-1]} 
    wget ftp://ftp.ncbi.nlm.nih.gov/geo/series/${GSE[0..-4]}nnn/${GSE}/miniml/${GSE}_family.xml.tgz
    tar -xzvf ${GSE}_family.xml.tgz
    """
}

process GET_CSV_FROM_XML {
    /// VERY provisional, I just need to iterate this process over several GSE and check the result
    /// The publishing directory will be the one of the study
    publishDir "/home/121109636/CSV_reports"


    input:
    path xml_report

    output:
    path "*.csv"

    script:
    """
    python3 $projectDir/scripts/xml_parsing.py  ${xml_report}
    """
}


workflow {
    input = Channel.of( "GSE180669","GSE156796", "GSE185286", "GSE185458","GSE158141",
"GSE173856","GSE136940","GSE130465","GSE157361","GSE157423","GSE152554","GSE152556",
"GSE152558","GSE167704","GSE167223","GSE166874","GSE160917" ) 
    GET_GSE_REPORT          ( input )
    GET_CSV_FROM_XML        ( GET_GSE_REPORT.out )
}
