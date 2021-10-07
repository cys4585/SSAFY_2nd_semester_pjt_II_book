
pipeline {
    agent none

    options { skipDefaultCheckout(true) }

    stages {
        stage('Build and Test') {
            // docker image에 명시된 image를 활용하여 steps 수행
            agent {
                docker { 
                    image 'python:3.9.7'
                    args '-v /$HOME/.m2:/root/.m2'
                } 
            } 
            options { skipDefaultCheckout(false) }
            steps {
                // sh 'python [백 이미지 경로] test ./ISEAU'
                sh 'python --version'
            }  
        }
        
        stage('Docker build') {
            agent any
            steps {
                // docker build -t [이미지 이름] [경로]
                sh 'docker build -t frontend:latest ./frontend'
                sh 'docker build -t backend:latest ./backend'
            }
        }

        stage('Docker run') {
            agent any
            steps {
                // 현재 동작중인 컨테이너 중 name='OO'의 이름을 가진 컨테이너를 stop한다.
                sh 'docker ps -f name=frontend -q | xargs --no-run-if-empty docker container stop'
                sh 'docker ps -f name=backend -q | xargs --no-run-if-empty docker container stop'
                // <front-image_name>의 이름을 가진 컨테이너를 삭제한다.
                sh 'docker container ls -a -f name=frontend -q | xargs -r docker container rm'
                sh 'docker container ls -a -f name=backend -q | xargs -r docker container rm'
                // docker image build 시 기존에 존재하던 이미지는 dangling 상태가 되기 때문에 이미지를 일괄 삭제
                sh 'docker images -f "dangling=true" -q | xargs -r docker rmi'
                // docker container 실행
                sh 'docker run -d --name frontend -p 80:80 frontend:latest'
                sh 'docker run -d --name backend -p 8000:8000 backend:latest'
            }
        }
    } 
}

// pipeline {
//     agent any
    
//     tools {
//         nodejs "nodejs"
//     }

//     parameters {
//         string(name: 'GIT_URL', defaultValue: 'https://lab.ssafy.com/s05-bigdata-rec/S05P21D203.git', description: 'GIT_URL')
//         booleanParam(name: 'VERBOSE', defaultValue: false, description: '')
//     }

//     environment {  
//         GIT_BUSINESS_CD = 'develop'
//         GIT_CREDENTIAL_ID = 'test2'
//         VERBOSE_FLAG = '-q'
//     }

//     stages{
//         stage('Preparation'){ 
//             steps{
//                 script{
//                     env.ymd = sh (returnStdout: true, script: ''' echo date '+%Y%m%d-%H%M%S' ''')
//                 }
//                 echo("params : ${env.ymd} " + params.tag)
//             }
//         }

//         stage('Checkout'){ 
//             steps{
//                 git(branch: "${env.GIT_BUSINESS_CD}",
//                 credentialsId: "${env.GIT_CREDENTIAL_ID}", url: params.GIT_URL, changelog: false, poll: false)
//             }
//         }

//         // stage('Build'){
//         //     steps{
//         //         dir('frontend'){
//         //             sh 'pwd'
//         //             sh 'ls'
//         //             sh 'npm install'
//         //             sh 'npm run build'
//         //         } 
//         //     }
//         // }

//         // stage('Docker build') {
//         //     steps {
//         //         sh 'ls'
//         //         sh 'docker-compose up --build'
//         //     }
//         // }

//         stage('Docker build') {
//             angent any
//             steps {
//                 sh 'docker build -t s05p21d203_backend:latest'
//             }
//         }
//     }
// }

// ====================================================================================================================
// ====================================================================================================================
// ====================================================================================================================

// pipeline{
//     agent any
//     tools {nodejs "nodejs"}

//     environment {
//         GIT_BUSINESS_CD = 'develop'
//         GIT_CREDENTIAL_ID = 'iiilll_iill@naver.com'
//         VERBOSE_FLAG = '-q'
//     }

//     stages{
//         stage('Preparation'){
//             steps{
//                 script{
//                     env.ymd = sh (returnStdout: true, script: ''' echo date '+%Y%m%d-%H%M%S' ''')
//                 }
//                 echo("params : ${env.ymd} " + params.tag)
//             }
//         } 

//         stage('Build'){
//             steps{
//                 dir('frontend'){
//                     sh 'pwd'
//                     sh 'npm install'
//                     sh 'npm run build'
//                 }
//             }
//         }

//         stage('Docker build'){
//             agent any
//             steps{
//                 sh 'docker build -t frontend:latest ./frontend'
//             }
//         }

//         stage('Front-end'){
//             agent{
//                 docker{image 'node:14-alpine'}
//             }
//             steps{
//                 sh 'node --version'
//             }
//         }

//     }
// }


// 젠킨스 파이프라인 플러그인을 호출하기 위한 블록 
// pipeline {  
//     // 파이프라인을 실행하고 싶은 위치 정의  
//     agent none
//     // gitlab의 소스를 jenkins 디렉토리로 내려받을 시  
//     // skipDefaultCheckout(true)일 경우 내려받는 프로세스 skip  
//     // skipDefaultCheckout(false)일 경우 gitlab 소스 체크 
//     options { skipDefaultCheckout(true) }  
//     // stage의 모음  
//     stages {   
//         // 실제 작업이 수행되는 블록   
//         // 해당 stage 명으로 jenkins 화면에 표시된다   
//         stage('Build and Test') {    
//             // docker image에 명시된 image를 활용하여 steps 수행    
//             agent {     
//                 docker {
//                     image 'maven:3.8-openjdk-11-slim'
//                     args '-v /$HOME/.m2:/root/.m2'
//                 }
//             }
//             options { skipDefaultCheckout(false) }    
//             steps {     
//                 sh 'mvn -B -DskipTests -f ./backend/webcuration clean package'    
//             }   
//         }   
//         stage('Docker build') {
//             agent any
//             steps {     
//                 sh 'docker build -t backend:latest ./backend/webcuration'     
//                 sh 'docker build -t frontend:latest ./frontend'    
//             }  
//         }   
//         stage('Docker run') {
//             agent any    
//             steps {
//                 // 현재 동작중인 컨테이너 중 frontend의 이름을 가진 컨테이너를 stop 한다     
//                 sh 'docker ps -f name=frontend -q | xargs --no-run-if-empty docker container stop'     
//                 // 현재 동작중인 컨테이너 중 backend의 이름을 가진 컨테이너를 stop 한다
//                 sh 'docker ps -f name=backend -q | xargs --no-run-if-empty docker container stop'
//                 // frontend의 이름을 가진 컨테이너를 삭제한다.     
//                 sh 'docker container ls -a -f name=frontend -q | xargs -r docker container rm'
//                 // backend의 이름을 가진 컨테이너를 삭제한다.
//                 sh 'docker container ls -a -f name=backend -q | xargs -r docker container rm'     
//                 // docker image build 시 기존에 존재하던 이미지는 dangling 상태가 되기 때문에 이미지를 일괄 삭제     
//                 sh 'docker images -f "dangling=true" -q | xargs -r docker rmi'     
//                 // docker container 실행     
//                 sh 'docker run -d --name backend -v /home/ubuntu/img:/home/img --network mokomoko -p 8080:8080 backend:latest'    
//                 sh 'docker run -d --name frontend -v /home/ubuntu/img:/home/img -v /home/ubuntu/key:/home/key --network mokomoko -p 80:80 -p 443:443 frontend:latest'     
//             }   
//         }  
//     } 
// }
