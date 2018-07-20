pipeline {
	
	agent { dockerfile true }

	stages {
		stage('Build image') {

			steps {
				/*node(label: 'docker-1.13') {
					script {
						def app = docker.build("getintodevops/hellonode")
					}
				}*/
				echo 'Build using Dockerfile'
			}
    	}

    stage('Test image') {
		steps {
			/*script {
				app.inside {
            		sh 'echo "Tests passed"'
        		}
			}*/	
			echo 'Test image stage'
		}   			
        
	}
    }
}
	