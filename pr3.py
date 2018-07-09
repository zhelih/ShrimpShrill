t = int(input())
for i in xrange(t):
  word = raw_input()
  possible = False
  for j in xrange(len(word)):
    if j == 0:
      continue
    pref = word[:j]
    if pref[len(pref)-1] == word[0]:
      a = pref[:len(pref)-1] + word
      if not a.startswith(word):
        print('Case #%d: %s' % (i+1, a))
        possible = True
        break
  if not possible:
    print('Case #%d: Impossible' % (i+1))
