tRED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
BLUE="\e[34m"
LIGHT_BLUE="\e[94m"
ENDCOLOR="\e[0m"

function kucharka() {
  if [[ $# -eq 0 || "$1" == "help" || "$1" == "--help" ]]; then
      >&2 echo ""

      if ! [[ "$PWD" == *"kucharka"* ]]; then
        >&2 echo -e " ${RED} You are probably not in your kucharka project location. Go there for this to work out. ${ENDCOLOR}"
        >&2 echo ""
      fi

      >&2 echo -e "  Hello! Welcome to collection of ${GREEN}kucharka helper scripts${ENDCOLOR}!"
      >&2 echo "  You can use following:"
      >&2 echo "  ----------------------"
      >&2 echo -e "  ${GREEN}test${ENDCOLOR} to run test suite"
      >&2 echo -e "  ${GREEN}update${ENDCOLOR} to import current database to your local machine"
      # >&2 echo -e "  ${GREEN}resdev${ENDCOLOR} to reset dev branch to current master, push it to dev server and restart it."
      # >&2 echo -e "    You can add ${LIGHT_BLUE}--hard${ENDCOLOR} to also reset database on dev server"
      >&2 echo -e "  ${GREEN}sync${ENDCOLOR} to reset local development db to production dump"
      >&2 echo ""
      return
  fi

  # run test suite
  RUN_TESTS=0
  TESTS_FAILED_ONLY=0
  TESTS_FAILED_FIRST=1

  # reset local database to production dump
  RESET_LOCAL_DB=0

  # reset dev server
  RESET_DEV=0
  RESET_DEV_SOFT=1
  RESET_DEV_HARD=0

  #
  INSTALL_PACKAGES=0
  INSTALL_NPM=0
  NPM_WATCH=0


  while test -n "$1"; do
    case "$1" in
      test|tests)
        RUN_TESTS=1
        while test -n "$2"; do
          case "$2" in
            --lf|--failed|failed)
              TESTS_FAILED_ONLY=1
              ;;
          esac
          shift
        done
        ;;
      update)
        RESET_LOCAL_DB=1
        INSTALL_PACKAGES=1
        INSTALL_NPM=1
        BUILD_WEBPACK=1
        ;;
      resdev)
        RESET_DEV=1
        while test -n "$2"; do
          case "$2" in
            --soft)
              RESET_DEV_SOFT=1
              RESET_DEV_HARD=0
              ;;
            --hard)
              RESET_DEV_SOFT=0
              RESET_DEV_HARD=1
              ;;
          esac
          shift
        done
        ;;
      sync)
        RESET_LOCAL_DB=1
        ;;
      watch)
        NPM_WATCH=1
        ;;
      esac
      shift
  done

  if [[ "$RUN_TESTS" -eq "1" ]]; then
    if [[ "$TESTS_FAILED_ONLY" -eq "1" ]]; then
      poetry run pytest --lf
    else
      poetry run pytest --ff
    fi
  fi

  if [[ "$RESET_LOCAL_DB" -eq "1" ]]; then
    (
      cd bin;
      . reset-local-db.sh kucharka sudo;
    )
    poetry run flask dev reset-passwords
  fi

  if [[ "$INSTALL_PACKAGES" -eq "1" ]]; then
    poetry install
  fi

  if [[ "$INSTALL_NPM" -eq "1" ]]; then
    (
      cd app/static
      npm ci
    )
  fi

  if [[ "$NPM_WATCH" -eq "1" ]]; then
    (
      cd app/static
      npm run watch
    )
  fi
}
