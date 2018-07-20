pipeline {
	
	agent { dockerfile true }

	stages {
		stage('Build image') {

			node(label: 'docker-1.13') {
				def app
		    	app = docker.build("getintodevops/hellonode")
			}
    	}

    stage('Test image') {
   			
        app.inside {
            sh 'echo "Tests passed"'
        }
	}
    }
}
	