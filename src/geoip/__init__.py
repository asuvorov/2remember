"""
(C) 2013-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

-------------------------------------------------------------------------------

Once the Middleware is added, you will be able to access City and/or Country Level Information
on the Request Object via the `geo_data` Dictionary, e.g.:

    >>> request.geo_data
    {
        "city":                 ""
        "continent_code":       "NA"
        "continent_name":       "North America"
        "country_code":         "US"
        "country_name":         "United States"
        "dma_code":             ""
        "is_in_european_union": False
        "latitude":             37.751
        "longitude":            -97.822
        "postal_code":          ""
        "region":               ""
        "time_zone":            "America/Chicago"
        "remote_addr":          "142.250.180.3"
    }

"""
