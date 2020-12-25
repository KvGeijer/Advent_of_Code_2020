import System.IO
import Data.List.Split (splitOn)
import Data.List
import Text.Read
import Data.Maybe

required :: [String]
required = ["byr:", "iyr:", "eyr:", "hgt:", "hcl:", "ecl:", "pid:"]

repl :: (Eq a) => a -> a -> [a] -> [a]
repl old new = map (\x -> if x == old then new else x)


-- Let's do a recursive one!
main :: IO ()
main = do
        input <- getContents
        let numOk = count input
        print numOk

count :: String -> Int
count  = sum . map valid . transform

okay :: String -> Bool
okay field = case (take 4 field) of
        "byr:" -> maybe False (\birth -> birth >= 1920 && birth <= 2002) birth' where birth' = readMaybe (drop 4 field) :: Maybe Int
        "iyr:" -> maybe False (\year -> year >= 2010 && year <= 2020) year' where year' = readMaybe (drop 4 field) :: Maybe Int
        "eyr:" -> maybe False (\year -> year >= 2020 && year <= 2030) year' where year' = readMaybe (drop 4 field) :: Maybe Int
        "hgt:" -> maybe False (\hgt -> if (unit == "cm") then hgt <= 193 && hgt >= 150 else if (unit == "in") then hgt >= 59 && hgt <= 76 else False) hgt' where 
                unit = drop ((length field)-2) field
                hgt' = readMaybe $ take ((length field)-6) (drop 4 field) :: Maybe Int
        "hcl:" -> (field !! 4) == '#' && (and . map haircol $ code) where code = drop 5 field
        "ecl:" -> elem col ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"] where col = drop 4 field 
        "pid:" -> (length num) == 9 where num = (drop 4 field)
        xs -> False


haircol :: Char -> Bool
haircol c = elem c "0123456789abcdef"

valid :: [String] -> Int
valid fields = (if (length list == 7) && (and list) then 1 else 0) where
                reduced = filter ( not . (=="cid:") . take 4) fields
                list =  [ okay field | field <- reduced]

transform :: String -> [[String]]
transform = map (splitOn " " . repl '\n' ' ') . splitOn "\n\n"


test1 = "ecl:ambpid:690616023byr:1994 iyr:2014 hgt:172cm hcl:#c0946f eyr:2022"

test2 = "eyr:1980 cid:97\nhcl:z ecl:#102145 iyr:2011 byr:1945\npid:187cm hgt:179in"
