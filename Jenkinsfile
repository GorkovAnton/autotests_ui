pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    parameters {
        string(name: 'WORKERS', defaultValue: '4', description: 'Потоки pytest-xdist')
        string(name: 'MARKER',  defaultValue: '',  description: 'Маркер pytest. Пусто = все тесты')
        string(name: 'RERUNS',  defaultValue: '1', description: 'Перезапуски упавших тестов')
    }

    environment {
        API_URL  = 'http://127.0.0.1:5050'
        HEADLESS = '1'
    }

    stages {
        stage('Install dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
    steps {
        sh '''
            . .venv/bin/activate

            mkdir -p allure-results

            pytest ${MARKER:+-m "$MARKER"} \
                -n "$WORKERS" \
                --reruns "$RERUNS" \
                --alluredir="$WORKSPACE/allure-results"
        '''
    }
}
    }

    post {
    always {
        script {
            echo "Workspace: ${env.WORKSPACE}"

            sh '''
                echo "Checking Allure results..."
                ls -lah "$WORKSPACE/allure-results" || true

                echo "JSON files:"
                find "$WORKSPACE/allure-results" \
                    -maxdepth 1 -name '*-result.json' -type f || true
            '''

            def resultFiles = sh(
                script: "find '$WORKSPACE/allure-results' -maxdepth 1 -name '*-result.json' -type f | wc -l",
                returnStdout: true
            ).trim().toInteger()

            if (resultFiles > 0) {
                allure(
                    includeProperties: false,
                    results: [[path: 'allure-results']]
                )
            } else {
                echo "No Allure test results found. Skipping report."
            }
        }

        archiveArtifacts(
            artifacts: 'allure-results/**, sut.log',
            allowEmptyArchive: true
        )
    }
}
}

