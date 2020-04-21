from conf import conf
from src import seeders


def seed():
    for seeder in conf.SEEDERS:
        getattr(seeders, seeder).seed()

    print("Seeding finished")
