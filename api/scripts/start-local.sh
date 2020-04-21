(
    flask drop &&
    flask db upgrade &&
    flask seed &&
    flask create:account -u orderwrite -p orderwrite -r 1 &&
    flask run --host=0.0.0.0
)
