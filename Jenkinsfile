pipeline {
	agent any

	stages {
		stage('Run docker') {
            
            steps {
                echo 'Run docker........'
                cd docker
                docker-compose up -d
                docker-compose logs -f selenium
            }
        }
	}
}