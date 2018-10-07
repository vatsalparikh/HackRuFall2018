# Address Standardizer - HackRuFall2018

An attempt at a fully internal address standardization and validation system.

---

# Thought Process

From the sample data set provided by Optum, it looked like for each mailing address entry there were six fields provided as input to the program:

* adr_ln_1_txt
* adr_ln_2_txt
* cty_nm
* st_cd
* zip_cd_txt
* cntry_cd

From the sample data set output and the given validation instructions that we were to process addresses "based on the provided zip code and state", we designed our project according to the following assumptions:

* all addresses would be United States mailing addresses
* recepient information is not included in the output
* if the state, five-digit zip code, and/or four-digit zip code extension are provided, then they are never invalid (but may need processing) and remaining fields may be invalid
* if any of these fields are missing, subsequent fields such as the city or street names are never invalid (but may need processing) and remaining fields may be invalid

---

# First Step: Sort the given fields of our address according to a blueprint.

Our mailing address blueprint consists of the following fields:

* `pa_nmbr` = primary address number
* `pa_pred` = primary address predirectional
* `pa_name` = primary address street name
* `pa_sufx` = primary address suffix
* `pa_posd` = primary address postdirectional
* `pa_pobx` = PO Box
* `sa_idnt` = secondary address identifier
* `sa_addr` = secondary address
* `extra` = aggregates values the parser is unable to classify
* `ll_city` = city
* `ll_stat` = state
* `ll_zip5` = five-digit ZIP code
* `ll_pls4` = four-digit extended portion of ZIP+4 code

Not all fields are required to be filled in (e.g. pa_pobx) in order for the mailing address to be considered complete.

A field for country is not provided, as we are assuming all mailing addresses are located in the United States.

---

# Second Step: Compare the major fields of the address to our database and make a list of all database entries that match with that field. Do this once for all major fields.

The [PostalPro *ZIP+4 Product* database](https://postalpro.usps.com/address-quality-solutions/zip-4-product) provides the following fields: (substrings assume an address entry is in string `entry`)

* `entry[58:68]` = primary address number (minimum)
* `entry[68:78]` = primary address number (maximum)
* `entry[22:24]` = primary address predirectional
* `entry[24:52]` = primary address entryeet name
* `entry[52:56]` = primary address suffix
* `entry[56:58]` = primary address postdirectional
* `entry[119:123]` = secondary address identifier
* `entry[123:131]` = secondary address
* `entry[131:139]` = secondary address
* `entry[177:183]` = city state key
* `entry[157:159]` = state
* `entry[1:6]` = five-digit ZIP code
* `entry[140:144]` = four-digit extended portion of ZIP+4 code (minimum)
* `entry[144:148]` = four-digit extended portion of ZIP+4 code (maximum)

The only field that is not directly provided is the city of the mailing address. Instead, it is presented in the form of a six-digit City State Key that can be looked up in another database called the [PostalPro *City State Product* database](https://postalpro.usps.com/address-quality/city-state-product). The relevant fields in that database are listed as follows: (substrings assume an address entry is in string `ctyst`)

* `ctyst[6:12]` = city state key
* `ctyst[13:41]` = city state name
* `ctyst[41:54]` = city state name abbreviation
* `ctyst[12:13]` = ZIP classification code

The ZIP Classification Code allows us to distinguish PO Boxes from normal mailing addresses, however no other information is provided on how they are represented in our *ZIP+4 Product* database (their sample data set did not include any), so in our project we just processed them with our primary address. Military addresses were also ignored in our implementation, as we did not see any of in Optum's sample data set and did not want to assume anything about the formatting of these fields from just what was mentioned about them in [(Section 2 of the USPS Postal Addressing Standards](https://pe.usps.com/text/pub28/welcome.htm).

City abbreviations are saved for use when validating addresses, as [the USPS prefers labels use the unabbreviated city names when possible](https://pe.usps.com/text/pub28/28c2_008.htm). However, because the USPS considers abbreviated city names acceptable rather than invalid, we decided not to prioritize enforcing this in our project either.

An interesting thing to note is that the PostalPro technical documentation seems to incorrectly list the substring of the City State Key in the *ZIP+4 Product* database. Testing its substring on the sample file provided gives the first letter and only four digits of the City State Key rather than the letter and all five digits.

The fields we sorted into our blueprint are then compared with the fields in these databases. Entries where one field matches with the other are saved into a list. This is done for all blueprint fields that are not blank, so that we end up with a list of entries for each non-empty field.

---

# Third Step: Compare lists with each other and look at entries they have in common.

If there is one match between all fields, we have a winner.

If not, then between the fields that do not match, compare for similarity and pick the most similar one
https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings
https://stackoverflow.com/questions/6690739/fuzzy-string-comparison-in-python-confused-with-which-library-to-use

We gave the fields in our blueprint priority importance as follows:
* state
* five-digit ZIP code
* four-digit extended portion of ZIP+4 code
* city
* [predirectional ]street name[ suffix][ postdirectional]
* primary address number (range)
* secondary address identifier\*
* secondary address\*

\*Considered non-essential: use closest matching entries when available, preserve in output if none found



# Areas of Improvement

Accounting for more edge cases and user input errors when standardizing and validating addresses (e.g. some unusual zip code inputs are accounted for, but not all of them), for instance:

* multiple hyphens in the input zip code field will likely result in an incorrect zip code parse
* PO Box addresses are processed correctly if they contain extraneous punctuation and whitespace, but not if the letters themselves are spelled wrong
* if there are multiple PO Boxes, only the last one is outputed in the final address

---

---

---


The given validation instructions were to do so "based on the provided zip code and state", so we assume that:
* these two fields will never be incorrect
* these two fields may be incomplete

https://pe.usps.com/text/pub28/28c2_012.htm
pa_nmbr = primary address number (range)
pa_pred = predirectional
pa_name = street name
pa_sufx = suffix
pa_posd = postdirectional
sa_idnt = secondary address identifier
sa_addr = secondary address
ll_city = city
ll_stat = state
ll_zip5 = five-digit ZIP code
ll_pls4 = four-digit extended portion of ZIP+4 code


State Abbreviation List
http://abbreviations.yourdictionary.com/articles/state-abbrev.html

"Hyphens in the address range are significant and are not removed. Hyphens in the street or city name, however, normally are not significant and may be replaced with a space."
https://pe.usps.com/text/pub28/28c2_013.htm

"The other exception is when the local address information unit has determined that one of the directional letters is used as an alphabet indicator and not as a directional."
https://pe.usps.com/text/pub28/28c2_014.htm

Leave directionals alone

Check to see if there are directionals at the ends of the string, if there are, try to match street names in the database to portions of the input street name. If one match is found, use that match. If multiple are found that are different, then ignore and leave it as is

If it's already abbreviated, leave it alone.

If it's not, leave it alone since USPS considers that acceptable


"If an address has two consecutive words that appear on the suffix table (Appendix C), abbreviate the second of the two words according to the suffix table and place it in the suffix field. The first of the two words is part of the primary name. Spell it out on the mailpiece in its entirety after the street name."
https://pe.usps.com/text/pub28/28c2_015.htm

"Numeric street names, for example, 7TH ST or SEVENTH ST, should be output on the mailpiece exactly as they appear in the ZIP+4 file."
https://pe.usps.com/text/pub28/28c2_016.htm



put them in prefix and suffix, check to see what's left inside pa_name, if the words left can all be abbbreviated according to C1 Street Suffix Abbreviations, then 