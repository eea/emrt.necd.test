pipeline {
	
	agent { dockerfile true }

	stages {
		stage('Build image') {

			steps {
				node(label: 'docker-1.13') {
				def app
		    	app = docker.build("getintodevops/hellonode")
				}
			}
    	}

    stage('Test image') {
		steps {
			app.inside {
            	sh 'echo "Tests passed"'
        	}	
		}   			
        
	}
    }
}
	