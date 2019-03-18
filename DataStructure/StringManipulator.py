
class Concatenate:
    
    def InfuseSeparator(self, main, separator=", ", splitter=" "):
        
        result = []
        if isinstance(main, list) is False:
            main = main.split(splitter)
        for characters in main:
            result.append(characters)
            result.append(separator)
        result.pop(-1)
        result = "".join(result)
        return result


class Enumerate:

    def CleanNumber(self, phrase):
        if phrase is not None:
            phrase = Manipulate().RemoveParts([".", ",", "Rp ", "rp ", " K", " k ", "Rp", "rp", "K", "k", " (", ") ", "(", ")", "%", " +", " +", "+"], phrase)
        return phrase

    def ReformToNumber(self, phrase):
        
        if phrase is not None:
            if "rb" in phrase:
                if "," in phrase:
                    phrase = Manipulate().ReplaceParts([[",", ""], ["rb", "00"]])
                elif "," not in phrase:
                    phrase = Manipulate().ReplaceParts(["rb", "000"])
            elif "k" in phrase:
                if "." in phrase:
                    phrase = Manipulate().ReplaceParts([[".", ""], ["k", "00"]])
                elif "." not in phrase:
                    phrase = Manipulate().ReplaceParts(["k", "000"])
            elif "K" in phrase:
                if "." in phrase:
                    phrase = Manipulate().ReplaceParts([[".", ""], ["K", "00"]])
                elif "." not in phrase:
                    phrase = Manipulate().ReplaceParts(["K", "000"])
            phrase = self.CleanNumber(phrase)
        return phrase


class Manipulate:

    def RemoveParts(self, parts, phrase):

        if phrase is not None:
            if isinstance(parts, list):
                for part in parts:
                    phrase = phrase.replace(part, "")
            else:
                phrase = phrase.replace(parts, "")
        return phrase

    def ReplaceParts(self, replacements, phrase):

        if phrase is not None:
            if isinstance(replacements[0], list):
                for replacement in replacements:
                    phrase = phrase.replace(replacement[0], replacement[1])
            else:
                phrase = phrase.replace(replacements[0], replacements[1])
        return phrase

    def RemoveLargeEmos(self, phrase):

        if phrase is not None:
            phrase = ''.join(char for char in phrase if len(char.encode('utf-8')) < 3)
        return phrase




