# Actual low-degree cochain modules and linear differentials

`HochschildCochainMaps.lean` uses nested R-linear maps for the actual bilinear, trilinear and four-linear cochain modules C², C³ and C⁴ of an associative R-algebra A. It constructs R-linear maps d²:C²→C³ and d³:C³→C⁴ with the full four- and five-face formulas.

When A has characteristic two, it proves `d3.comp d2 = 0`. All five audits compile without warnings and use only `propext` and `Quot.sound`. This is an actual complex at degree three, sufficient for a cycles-modulo-boundaries quotient there. No other degrees or Ext comparison are constructed in this file.
