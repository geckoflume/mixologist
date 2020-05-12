<!DOCTYPE html>
<html lang="en">

<head>
    <?php include('header.php') ?>
    <title>Mixologist</title>
</head>

<body id="page-top">

<!-- Page Wrapper -->
<div id="wrapper">
    <?php include('sidebar.php') ?>

    <!-- Content Wrapper -->
    <div id="content-wrapper" class="d-flex flex-column">

        <!-- Main Content -->
        <div id="content">
            <!-- Begin Page Content -->
            <div class="container-fluid">

                <!-- Page Heading -->
                <div class="d-sm-flex align-items-center justify-content-between mb-4">
                    <h1 class="h3 mb-0 text-gray-800">New recipe</h1>
                </div>
                <div class="row">
                    <!-- Content Column -->
                    <div class="col-xl-4 col-lg-5">
                        <!-- Project Card Example -->
                        <div class="card shadow mb-4">
                            <div class="card-header py-3">
                                <h6 class="m-0 font-weight-bold text-primary">Cocktail settings</h6>
                            </div>
                            <div class="card-body">
                                <form>
                                    <div class="form-group">
                                        <label for="exampleFormControlInput1">Name:</label>
                                        <input class="form-control form-control-solid" id="exampleFormControlInput1"
                                               type="text" placeholder="Cocktail name">
                                    </div>
                                    <div class="form-group">
                                        <label>Components:</label>
                                        <ul>
                                            <li>Vodka - 50mL</li>
                                        </ul>
                                    </div>
                                    <button type="submit" class="btn btn-danger ">Reset</button>
                                    <button type="submit" class="btn btn-primary float-right">Save cocktail</button>
                                </form>
                            </div>
                        </div>
                    </div>
                    <!-- Content Column -->
                    <div class="col-xl-8 col-lg-7">
                        <!-- Project Card Example -->
                        <div class="card shadow mb-4">
                            <div class="card-header py-3">
                                <h6 class="m-0 font-weight-bold text-primary">Add component</h6>
                            </div>
                            <div class="card-body">
                                <form>
                                    <div class="form-group">
                                        <label for="exampleFormControlSelect1">Select a component:</label>
                                        <select class="form-control form-control-solid" id="exampleFormControlSelect1">
                                            <option>Vodka</option>
                                            <option>Rhum</option>
                                            <option>Whiskey</option>
                                        </select>
                                    </div>
                                    <div class="form-group">
                                        <label for="capacityInput2">Volume (mL):</label>
                                        <input class="form-control form-control-solid" id="capacityInput2"
                                               type="number" min="0" step="5" placeholder="10">
                                    </div>
                                    <button type="submit" class="btn btn-primary float-right">Add</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- /.container-fluid -->
        </div>
        <!-- End of Main Content -->
    </div>
    <!-- End of Content Wrapper -->
</div>
<!-- End of Page Wrapper -->

<?php include('footer.php') ?>
</body>
</html>
