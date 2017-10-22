## MultiQC is used to generate final summary report containing statistics about multiple samples.  

There will be two separate reports for Long Ranger basic and ChromeQC  

### Run the code:  
 
`> ./preprocess_chromeqc.sh $folder_molecule_size`  
`> multiqc -f -c multiqc_config_chromeqc.yaml .`  
