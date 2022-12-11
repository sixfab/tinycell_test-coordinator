#!/bin/bash


COORDINATOR_REPO="https://github.com/sixfab/tinycell_test-coordinator"
TEST_PROCESS_REPO="https://github.com/sixfab/tinycell_test-process"
VERBOSE_SUFFIX="/dev/null"
# VERBOSE_SUFFIX="/dev/stdout"


print_help() {
    printf "[HELP]  $1\n"
}

print_info() {
    YELLOW='\033[0;33m'
    NC='\033[0m'
    printf "${YELLOW}[INFO]${NC}  $1\n"
}

print_error() {
    RED='\033[0;31m'
    NC='\033[0m'
    printf "${RED}[ERROR]${NC} $1\n"
}

print_done() {
    GREEN='\033[0;32m'
    NC='\033[0m'
    printf "${GREEN}[DONE]${NC}  $1\n"
}

run_command() {
    for count in {1..3}; do 
        COMMAND=$1
        sudo su sixfab -c "eval $COMMAND" &> $VERBOSE_SUFFIX
        STATUS_CODE=$?
        
        if [ $STATUS_CODE -eq "0" ]; then
            return
        fi
    done

    print_error "Installer faced an error during the following command, please re-run installer"
    print_error "*****************************************************"
    printf "\033[0;31m[ERROR]\033[0m $COMMAND\n"
    print_error "*****************************************************"
    exit 1
}

check_is_root() {
    if [ $(id -u) != 0 ]; then
        print_error "This script must be run as root"
        exit 1
    fi
}

create_sixfab_user() {
    sudo adduser --disabled-password --gecos "" sixfab &> $VERBOSE_SUFFIX
}

check_sixfab_folder() {
    if [ ! -d "/opt/sixfab" ]; then
        sudo mkdir /opt/sixfab
    fi

    if [ ! -d "/opt/sixfab/tinycell" ]; then
        sudo mkdir /opt/sixfab/tinycell
    fi

    sudo chown sixfab /opt/sixfab
    sudo chown sixfab /opt/sixfab/tinycell
}

initialize_sudoers() {
    print_info "Updating sudoers..."
    echo "sixfab ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/sixfab_tinycell &> $VERBOSE_SUFFIX
    print_info "Sudoers updated"
}

check_system_dependencies() {
    git --version &> $VERBOSE_SUFFIX
    IS_GIT_INSTALLED=$?
    python3 --version &> $VERBOSE_SUFFIX
    IS_PYTHON_INSTALLED=$?
    pip3 --version &> $VERBOSE_SUFFIX
    IS_PIP_INSTALLED=$?
    if [ ! "$IS_GIT_INSTALLED" = "0" ] || \
       [ ! "$IS_PYTHON_INSTALLED" = "0" ] || \
       [ ! "$IS_PIP_INSTALLED" = "0" ]; then
        install_system_dependencies
    fi
}


install_system_dependencies() {
    print_info "Looking for dependencies..."

    # Check if git installed
    if ! [ -x "$(command -v git)" ]; then
        print_info 'Git is not installed, installing...'
        run_command "sudo apt install git -y"
    fi

    # Check if python3 installed
    if ! [ -x "$(command -v python3)" ]; then
        print_info 'Python3 is not installed, installing...'
        run_command "sudo apt install python3 -y"
    fi

    # Check python3 version, minimum python3.6 required
    version=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)' | sed -e 's/\.//g')

    if [ "$version" -lt "360" ]; then
        print_error "Python 3.6 or later version is required to run Sixfab Tinycell Test. 
        Please upgrade Python and re-try. Using latest version of Raspberry Pi OS is recommended."
        exit
    fi

    # Check if pip3 installed
    if ! [ -x "$(command -v pip3)" ]; then
        print_info 'Pip for python3 is not installed, installing...'
        run_command "sudo apt install python3-pip -y"
    fi

    check_system_dependencies
}


install_coordinator() {
    if [ -d "/opt/sixfab/tinycell/tinycell_test-coordinator" ]; then
        print_info "Coordinator source already exists, updating..."
        git -C /opt/sixfab/tinycell/tinycell_test-coordinator reset --hard HEAD &> $VERBOSE_SUFFIX
        git -C /opt/sixfab/tinycell/tinycell_test-coordinator pull &> $VERBOSE_SUFFIX
    else
        print_info "Downloading coordinator source..."
        git clone $COORDINATOR_REPO /opt/sixfab/tinycell &> $VERBOSE_SUFFIX
    fi
    
    # Create and activate virtual environment
    python3 -m venv coordinator_env
    source coordinator_env/bin/activate

    print_info "Installing dependencies..."
    run_command "pip3 install -r /opt/sixfab/tinycell/tinycell_test-coordinator/requirements.txt --no-cache-dir"
    
    print_info "Installed dependencies."
    print_info "Initializing service..."

    sudo cp /opt/sixfab/tinycell/tinycell_test-coordinator/tinycell_test-coordinator.service \
    /etc/systemd/system/tinycell_test-coordinator.service &> $VERBOSE_SUFFIX

    sudo chown sixfab /etc/systemd/system/tinycell_test-coordinator.service &> $VERBOSE_SUFFIX
    sudo systemctl daemon-reload &> $VERBOSE_SUFFIX
    sudo systemctl enable tinycell_test-coordinator.service &> $VERBOSE_SUFFIX
    sudo systemctl restart tinycell_test-coordinator.service &> $VERBOSE_SUFFIX

    print_info "tinycell_test-coordinator service initialized successfully."
}


# Main Function of installer
run() {
    check_is_root
    create_sixfab_user
    check_sixfab_folder
    initialize_sudoers
    check_system_dependencies
    
    # TODO: Activate this if repos are public in the future 
    # install_coordinator
}

# Run installer
run
