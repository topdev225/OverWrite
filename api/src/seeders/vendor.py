import mimesis
from safrs import DB as db

from src import models


class VendorSeeder:
    @staticmethod
    def seed():
        address = mimesis.Address()
        business = mimesis.Business()
        person = mimesis.Person()

        vendor_types = [
            {"is_supplier": True},
            {"is_decorator": True},
            {"is_pick_pack": True},
            {"is_supplier": True, "is_pick_pack": True},
            {"is_decorator": True, "is_pick_pack": True},
        ]

        product_types = models.ProductType.query.all()

        # create five vendors for each product type
        for product_type in product_types:
            for vendor_type in vendor_types:
                vendor = models.Vendor(
                    name=f"{address.state()} {business.company()}",
                    email=person.email(),
                    address=address.address(),
                    **vendor_type,
                )

                product_type.vendors.append(vendor)

                db.session.add(vendor)
                db.session.add(product_type)
                db.session.commit()
