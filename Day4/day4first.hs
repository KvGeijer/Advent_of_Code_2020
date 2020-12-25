import System.IO
import Data.List.Split (splitOn)
import Data.List (isSubsequenceOf, delete)

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

--count :: String -> Int
count  = sum . map valid'' . transform

--valid :: [String] -> Int
valid fields = let      deleted = foldl (\acc field -> if elem (take 4 field) acc then delete (take 4 field) acc else acc) required fields
                        len = length fields
                        lendel = length deleted
                        in (deleted, fields)
                        --in if (len - lendel == 7) then 1 else 0

valid'' fields = (if (length list == 7) && (and list) then 1 else 0) where
                reduced = filter ( not . (=="cid:") . take 4) fields
                list =  [ elem (take 4 field) required | field <- reduced]

transform :: String -> [[String]]
transform = map (splitOn " " . repl '\n' ' ') . splitOn "\n\n"

--count' :: String -> Int
--count' = sum . map valid . splitOn "\n\n" 

--valid' :: String -> Int
--valid' string = if and [ isSubsequenceOf req string |req <- required] then
--        1 else 0


test1 = "ecl:ambpid:690616023byr:1994 iyr:2014 hgt:172cm hcl:#c0946f eyr:2022"

test2 = "eyr:1980 cid:97\nhcl:z ecl:#102145 iyr:2011 byr:1945\npid:187cm hgt:179in"
