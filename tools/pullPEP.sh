#!/bin/bash

# pull or clone burningToast and run lint checks on it.
# make sure to have a ssh key setup for bitbucket access

repoUrl="git@bitbucket.org:mbvdlza/burningtoast.git"
repoRoot="$HOME/tmp/"
repoPath="burningtoast"
gitPath=$(whereis -b git | awk '{print $2}')
#pylintPath=$(whereis -b pylint | awk '{print $2}')
pep8Path=$(command -v pep8)
seemsOK=false
mailRecipients="marlon@kbye.co.za,marlon@rightshift.biz"
mailContent="$HOME/tmp/mail"
testBranch="dev"
todayDate=$(date)

echo "______________ Nightly PEP8 report for $repoPath for $todayDate ___________" > $mailContent
echo " " >> $mailContent

if [ -z $pep8Path ];
then
    echo "pep8 must be installed... ciao." >> $mailContent
    exit
fi

# cehck if pep8 is available or exit

echo "trying $repoRoot$repoPath" >> $mailContent

if [ ! -d $repoRoot$repoPath ];
then
    echo "$repoRoot$repoPath does not exist... trying to clone it"; >> $mailContent
    cd $repoRoot;
    $gitPath clone $repoUrl >> $mailContent;
    seemsOK=true
    echo " " >> $mailContent
else
    echo "$repoRoot$repoPath exists, trying to pull" >> $mailContent;
    cd $repoRoot$repoPath;
    $gitPath pull >> $mailContent >> $mailContent;
    seemsOK=true
    echo " " >> $mailContent
fi

if [ $seemsOK ];
then
    echo " " >> $mailContent
    echo "============ pep8 report start ==========================================" >> $mailContent;
    cd $repoRoot$repoPath;
    $gitPath checkout --track -b $testBranch origin/$testBranch >> $mailContent;
    $pep8Path --exclude=*.md * >> $mailContent;
    echo "=========================================================================" >> $mailContent;
    echo " " >> $mailContent
    echo "Ok, Bye!" >> $mailContent
fi

cat $mailContent | /usr/bin/mail -s "$repoPath pep8 : Nightly Report for $todayDate" $mailRecipients

