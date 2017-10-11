<?php
	$conn = new mysqli("", "", "", "");


	$query = "SELECT * FROM NJITParking WHERE deck != 'FENS1' AND deck != 'FENS2' AND deck != 'Lot 10' AND entered > (NOW() - INTERVAL 30 DAY);";
	$stmt = $conn->prepare($query);
	$stmt->execute();
	$stmt->store_result();
	$stmt->bind_result($deck, $available, $occupied, $total,$entered);

	echo "deck,available,occupied,total,entered\n";
	while ($stmt->fetch())
	{
		echo "$deck,$available,$occupied,$total,$entered\n";
	}
?>
