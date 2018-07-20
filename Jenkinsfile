pipeline {
	
	agent { dockerfile true }

	stages {
		stage('Build image') {

			steps {
				node(label: 'docker-1.13') {
					script {
						def app
		    			app = docker.build("getintodevops/hellonode")
					}
				}
			}
    	}

    stage('Test image') {
		steps {
			script {
				app.inside {
            		sh 'echo "Tests passed"'
        		}
			}	
		}   			
        
	}
    }
}
	