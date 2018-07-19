pipeline {
	agent any

	stages {
		stage('Run docker') {
            
            steps {
                sh `echo 'Run docker........'`
                sh `cd docker`
                sh `docker-compose up -d`
                sh `docker-compose logs -f selenium`
            }
        }
	}
}