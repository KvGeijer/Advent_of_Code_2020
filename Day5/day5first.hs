import System.IO
--import Data.List.Split (splitOn)
import Data.List (sort)


main :: IO ()
main = do
        input <- fmap lines getContents
        let highest = findMax input
        print highest


findMax :: [String] -> Int
findMax = findMissing . sort . map (decode . toBinary . take 10) 

findMissing :: [Int] -> Int
findMissing (x : y : xs) = if x + 1 == y then findMissing (y:xs) else x+1

decode :: String -> Int
decode = fromBinary . reverse 


fromBinary :: [Char] -> Int
fromBinary [] = 0
fromBinary (x:xs) = (read [x] :: Int) + 2 * (fromBinary xs)

--decouple :: String -> (String, String)
--decouple string = (take 7 string, drop 7 string)

toBinary :: [Char] -> String
toBinary [] = []
toBinary (x:xs)
        | x == 'F'      = '0' : toBinary xs
        | x == 'B'      = '1' : toBinary xs
        | x == 'L'      = '0' : toBinary xs
        | x == 'R'      = '1' : toBinary xs
        | otherwise       = "9"
        
        
        