from safrs import DB as db


class LocationSeeder:
    @staticmethod
    def seed():

        # text = Text()
        # address = Address()
        # person = Person()
        #
        # campaigns = models.Campaign.query.all()
        #
        # for campaign in campaigns:
        #     location = models.Location(
        #         campaign=campaign,
        #         nickname=text.word(),
        #         company_name=text.word(),
        #         street_and_number=f'{address.street_name()} '
        #                           f'{address.street_number()}',
        #         city=address.city(),
        #         zip_code=address.zip_code(),
        #         delivery_contact=person.full_name(),
        #         suite_unit_etc=text.word(),
        #         region=address.state(),
        #         country=address.country())
        #     db.session.add(location)

        db.session.commit()
