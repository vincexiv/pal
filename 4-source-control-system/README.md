## About
This is a simple distributed source control system made in the style of Git

## To run the project <br />
`./vcs.py <command> <args>` <br/>

## The commands supported include;
- init
- add
- commit
- log
- branch
- checkout
- status

## Reservation
- The work is not implemented in the exact way git does it. For instance, running `./vcs.py status` does not show 
a diff between what is in our working directory versus what is in the index, versus what is committed