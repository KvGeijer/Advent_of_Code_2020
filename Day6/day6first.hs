import System.IO
import Data.List.Split (splitOn)
import Data.List (reverse, nub)


main = do interact (show . sum . map (length . nub . filter (/= '\n')) ) . splitOn ("\n\n") . filter (/= '\r')) )


