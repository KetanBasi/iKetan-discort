# SECTION: Configuration
# ANCHOR: Release Status
# value (uppercase allowed):
#   - alpha     ()
#   - beta      ()
#   - rc        (release candidate)
#   - stable    (released)
release_status = 'alpha'.lower()

presence_image_url = 'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/8a37d87d-a6e5-4ad9-9c67-02a8842ca36b/dbpr9n8-773872ad-74cc-4124-8458-dbce41771acd.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvOGEzN2Q4N2QtYTZlNS00YWQ5LTljNjctMDJhODg0MmNhMzZiXC9kYnByOW44LTc3Mzg3MmFkLTc0Y2MtNDEyNC04NDU4LWRiY2U0MTc3MWFjZC5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ._R8hTZ0Uzfh5Pl_BClZ7WgmI7TJugP5-s9r3YOBXo8U'

# !SECTION: Configuration








RelAlpha = release_status == 'alpha'
RelBeta = release_status == 'beta'
RelRC = release_status == 'rc'
RelStable = release_status == 'stable'








