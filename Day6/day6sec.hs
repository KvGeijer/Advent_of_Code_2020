import System.IO
import Data.List.Split (splitOn)
import Data.List (reverse, nub)


main :: IO ()
main = do interact (show . solve . splitOn ("\n\n") . filter (not . (== '\r')) )

solve :: [String] -> Int
solve = sum . map (count . lines)

count :: [String] -> Int
count [xs]              = length xs
count ([]:xs)           = 0
count ((y:ys):xs)       = (val + count (ys:xs)) where 
        val = if (and (map (elem y) xs)) then 1 else 0 