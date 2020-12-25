import System.IO  
import Data.List
import Data.Maybe

createMat :: [Int] -> [[Bool]]
createMat list = [[x+y == 2020| x <- list]| y <- list]

makeIntegers :: String -> [Int]
makeIntegers = (map read).lines


main :: IO ()
main = do
	inputStrings <- getContents
	let 	
		input = makeIntegers inputStrings
		filtMat = createMat input
		flat = map or filtMat
		i = fromJust $ elemIndex True flat
		j = fromJust $ elemIndex True (filtMat !! i)
		first = input !! i
		second = input !! j
		mult = first * second
	print first
	print second
	print mult

		
		
	


	