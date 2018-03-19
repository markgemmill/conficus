#### TODO

* verify unicode capable?
* parse nested lists/tuples
* add coercion for urls?
* define and document readonly mode
* make sure lists are converted to tuples in
  readonly mode
* add interpolation of strings?
* add validation hooks and doc samples
* test adding custom user coercions
* clean up and unify test suite
    - we have multiple tests covering the same ground


#### DONE

* ~~switch docs to sphinx~~
* ~~set up docs on readthedocs~~
* ~~work out method of linking README.md with docs/docs/index.md~~
* ~~allow for properly readable format of ConfigDict~~
  - ~~doesn't need to be reprint of source.~~
  - ~~as long as its readable in the console or log.~~
  - ~~make sure password fields are obfuscated.~~


#### DISCARDED
We're not going for serialization here...
* ~~allow for TOML style multiline strings?~~
* ~~add dumps/format functionality?~~
