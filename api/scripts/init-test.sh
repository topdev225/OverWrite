(
    flask drop &&
    flask db upgrade &&
    flask seed &&
    flask create:account -u admin -p admin -r 1
)