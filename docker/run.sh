#!/bin/bash

# We do this because the entry point order defined in setup.py is not ensured.
# Our tests need to run in a specific order, such as the portal gets created,
# tests run and then the portal gets deleted.

TESTS=(
    setup_tests
    review_folder
    finish_observation
    deny_observation
    add_answer
    finish_observation_lr
    ask_to_redraft
    add_conclusions
    remove_test_site
)

COMMAND_RUN="/home/selenium/.local/bin/seleniumtesting -v -B chrome -P /usr/bin/chromedriver -A='--headless' -sw 3840 -sh 2160 http://plone:8080/Workflow_test"
COMMAND_ARGS="-ea ldap_credentials $LDAP_USER $LDAP_PASSWORD -ea zope_user $ZOPE_USER $ZOPE_PASSWORD -ea roles sectorexpert $EXPERT_USER -ea users $EXPERT_USER $EXPERT_PASSWORD -ea roles leadreviewer $REVIEW_USER -ea users $REVIEW_USER $REVIEW_PASSWORD -ea roles msauthority $AUTHORITY_USER -ea users $AUTHORITY_USER $AUTHORITY_PASSWORD"

for x in ${TESTS[@]};
do
    COMMAND="$COMMAND_RUN emrt.necd.test.$x $COMMAND_ARGS";
    bash -c "$COMMAND"
done
