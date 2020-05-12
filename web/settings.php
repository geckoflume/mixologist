<!DOCTYPE html>
<html lang="en">

<head>
    <?php include('header.php') ?>
    <title>Mixologist - Settings</title>
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
                    <h1 class="h3 mb-0 text-gray-800">Settings</h1>
                </div>
                <div class="row">
                    <!-- Content Column -->
                    <div class="col-lg">
                        <!-- Project Card Example -->
                        <div class="card shadow mb-4">
                            <div class="card-header py-3">
                                <h6 class="m-0 font-weight-bold text-primary">Glass configuration</h6>
                            </div>
                            <div class="card-body">
                                <form>
                                    <div class="form-group">
                                        <label for="capacityInput2">Capacity (mL):</label>
                                        <input class="form-control form-control-solid" id="capacityInput2"
                                               type="number" min="0" step="5" placeholder="700">
                                    </div>
                                    <div class="form-group">
                                        <label for="level4">Current level (mL):</label>
                                        <input class="form-control form-control-solid" id="level4"
                                               type="number" min="0" step="5" disabled>
                                    </div>
                                    <button type="submit" class="btn btn-secondary">Load cell tare</button>
                                    <button type="submit" class="btn btn-primary float-right">Apply</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Content Row -->
                <div class="row">
                    <!-- Content Column -->
                    <div class="col-lg">
                        <!-- Project Card Example -->
                        <div class="card shadow mb-4">
                            <div class="card-header py-3">
                                <h6 class="m-0 font-weight-bold text-primary">Bottle 1 configuration</h6>
                            </div>
                            <div class="card-body">
                                <form>
                                    <div class="form-group">
                                        <div class="custom-control custom-checkbox">
                                            <input class="custom-control-input" id="enableBottle1" type="checkbox">
                                            <label class="custom-control-label" for="enableBottle1">Enabled</label>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <label for="exampleFormControlInput1">Name:</label>
                                        <input class="form-control form-control-solid" id="exampleFormControlInput1"
                                               type="text" placeholder="Bottle name">
                                    </div>
                                    <div class="form-group">
                                        <label for="capacityInput1">Capacity (mL):</label>
                                        <input class="form-control form-control-solid" id="capacityInput1"
                                               type="number" min="0" step="5" placeholder="700">
                                    </div>
                                    <div class="form-group">
                                        <label for="level4">Current level (mL):</label>
                                        <input class="form-control form-control-solid" id="level4"
                                               type="number" min="0" step="5" disabled>
                                    </div>
                                    <button type="submit" class="btn btn-secondary">Load cell tare</button>
                                    <button type="submit" class="btn btn-primary float-right">Apply</button>
                                </form>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg">
                        <!-- Project Card Example -->
                        <div class="card shadow mb-4">
                            <div class="card-header py-3">
                                <h6 class="m-0 font-weight-bold text-primary">Bottle 2 configuration</h6>
                            </div>
                            <div class="card-body">
                                <form>
                                    <div class="form-group">
                                        <div class="custom-control custom-checkbox">
                                            <input class="custom-control-input" id="enableBottle2" type="checkbox">
                                            <label class="custom-control-label" for="enableBottle2">Enabled</label>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <label for="exampleFormControlInput1">Name:</label>
                                        <input
                                                class="form-control form-control-solid" id="exampleFormControlInput1"
                                                type="text" placeholder="Bottle name">
                                    </div>
                                    <div class="form-group">
                                        <label for="capacityInput2">Capacity (mL):</label>
                                        <input class="form-control form-control-solid" id="capacityInput2"
                                               type="number" min="0" step="5" placeholder="700">
                                    </div>
                                    <div class="form-group">
                                        <label for="level4">Current level (mL):</label>
                                        <input class="form-control form-control-solid" id="level4"
                                               type="number" min="0" step="5" disabled>
                                    </div>
                                    <button type="submit" class="btn btn-secondary">Load cell tare</button>
                                    <button type="submit" class="btn btn-primary float-right">Apply</button>
                                </form>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg">
                        <!-- Project Card Example -->
                        <div class="card shadow mb-4">
                            <div class="card-header py-3">
                                <h6 class="m-0 font-weight-bold text-primary">Bottle 3 configuration</h6>
                            </div>
                            <div class="card-body">
                                <form>
                                    <div class="form-group">
                                        <div class="custom-control custom-checkbox">
                                            <input class="custom-control-input" id="enableBottle3" type="checkbox">
                                            <label class="custom-control-label" for="enableBottle3">Enabled</label>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <label for="exampleFormControlInput1">Name:</label>
                                        <input class="form-control form-control-solid" id="exampleFormControlInput1"
                                               type="text" placeholder="Bottle name">
                                    </div>
                                    <div class="form-group">
                                        <label for="capacityInput3">Capacity (mL):</label>
                                        <input class="form-control form-control-solid" id="capacityInput3"
                                               type="number" min="0" step="5" placeholder="700">
                                    </div>
                                    <div class="form-group">
                                        <label for="level4">Current level (mL):</label>
                                        <input class="form-control form-control-solid" id="level4"
                                               type="number" min="0" step="5" disabled>
                                    </div>
                                    <button type="submit" class="btn btn-secondary">Load cell tare</button>
                                    <button type="submit" class="btn btn-primary float-right">Apply</button>
                                </form>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg">
                        <!-- Project Card Example -->
                        <div class="card shadow mb-4">
                            <div class="card-header py-3">
                                <h6 class="m-0 font-weight-bold text-primary">Bottle 4 configuration</h6>
                            </div>
                            <div class="card-body">
                                <form>
                                    <div class="form-group">
                                        <div class="custom-control custom-checkbox">
                                            <input class="custom-control-input" id="enableBottle4" type="checkbox">
                                            <label class="custom-control-label" for="enableBottle4">Enabled</label>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <label for="exampleFormControlInput1">Name:</label>
                                        <input class="form-control form-control-solid" id="exampleFormControlInput1"
                                               type="text" placeholder="Bottle name">
                                    </div>
                                    <div class="form-group">
                                        <label for="capacityInput4">Capacity (mL):</label>
                                        <input class="form-control form-control-solid" id="capacityInput4"
                                               type="number" min="0" step="5" placeholder="700">
                                    </div>
                                    <div class="form-group">
                                        <label for="level4">Current level (mL):</label>
                                        <input class="form-control form-control-solid" id="level4"
                                               type="number" min="0" step="5" disabled>
                                    </div>
                                    <button type="submit" class="btn btn-secondary">Load cell tare</button>
                                    <button type="submit" class="btn btn-primary float-right">Apply</button>
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
