<?php $page = basename($_SERVER['SCRIPT_NAME']); ?>
<!-- Sidebar -->
<ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">

    <!-- Sidebar - Brand -->
    <a class="sidebar-brand d-flex align-items-center justify-content-center" href="index.html">
        <div class="sidebar-brand-icon rotate-n-15">
            <i class="fas fa-glass-citrus"></i>
        </div>
        <div class="sidebar-brand-text mx-3">Mixologist</div>
    </a>

    <!-- Divider -->
    <hr class="sidebar-divider my-0">

    <!-- Nav Item - Dashboard -->
    <li class="nav-item <?php echo $page == 'index.php' ? 'active' : '' ?>">
        <a class="nav-link" href="index.php">
            <i class="fas fa-fw fa-tachometer-alt"></i>
            <span>Dashboard</span></a>
    </li>

    <!-- Divider -->
    <hr class="sidebar-divider">

    <!-- Heading -->
    <div class="sidebar-heading">
        Recipes
    </div>

    <!-- Nav Item - New recipe -->
    <li class="nav-item <?php echo $page == 'list_recipes.php' ? 'active' : '' ?>">
        <a class="nav-link" href="list_recipes.php">
            <i class="fas fa-fw fa-list-ul"></i>
            <span>List recipes</span></a>
    </li>

    <!-- Nav Item - New recipe -->
    <li class="nav-item <?php echo $page == 'new_recipe.php' ? 'active' : '' ?>">
        <a class="nav-link" href="new_recipe.php">
            <i class="fas fa-fw fa-plus-circle"></i>
            <span>Add new recipe</span></a>
    </li>

    <!-- Divider -->
    <hr class="sidebar-divider">

    <!-- Heading -->
    <div class="sidebar-heading">
        Settings
    </div>

    <!-- Nav Item - Settings -->
    <li class="nav-item <?php echo $page == 'settings.php' ? 'active' : '' ?>">
        <a class="nav-link" href="settings.php">
            <i class="fas fa-fw fa-cog"></i>
            <span>Settings</span></a>
    </li>

    <!-- Divider -->
    <hr class="sidebar-divider d-none d-md-block">

    <!-- Sidebar Toggler (Sidebar) -->
    <div class="text-center d-none d-md-inline">
        <button class="rounded-circle border-0" id="sidebarToggle"></button>
    </div>

</ul>
<!-- End of Sidebar -->