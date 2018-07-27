pipeline {
    agent any

    stages {
        stage('Build & Test') {
            steps {
                node(label: 'docker'){
                    try {
                        checkout scm
                        sh "echo 'Building stuff.......'" 
                        sh "docker build -t ${BUILD_TAG} ."
                    }
                    finally {
                        sh "echo 'DONEEEEEE!"
                    }
                }
            }
        }
    }
}
