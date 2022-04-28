#!/bin/zsh

for i in "01" "02" "03" "04"
do
  for s in "5" "10" "20" "30" "40" "50" "75" "100" "250" "500" "750" "1000"
    do
    for g in "guess" "guess_sophisticated"
    do
      for f in "filter" "filter_sophisticated"
      do
        printf "%s,%s,%s,%s," "$i" "$s" "$g" "$f"
        l="$(echo "\n\nmaxtime($s).\n" | cat "logic_programs/${i}_inst_windy.lp" "logic_programs/vanilla/${f}.lp" "logic_programs/vanilla/${g}.lp" "logic_programs/vanilla/opt.lp" - | clingo --text | wc -l)"
        printf "%s," "$l"
        w="$(echo "\n\nmaxtime($s).\n" | cat "logic_programs/${i}_inst_windy.lp" "logic_programs/vanilla/${f}.lp" "logic_programs/vanilla/${g}.lp" "logic_programs/vanilla/opt.lp" - | clingo --models 0 --time-limit 30 --quiet=2 --parallel-mode 16,compete)"
        o="$(printf "%s" $w | grep -F "Optimization" | grep -z -Eo "[0-9]+ [0-9]+")"
        b="$(printf "%s" $w | grep -F "Bounds" | grep -z -Eo "\[.*\]")"
        printf "%s,%s\n" "$o" "$b"
      done
    done
  done
done
