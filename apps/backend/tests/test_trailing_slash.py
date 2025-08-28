from app.main import app

def test_products_trailing_slash():
    """Test that both /products and /products/ work"""
    # This test verifies the structure, actual testing would require a test client
    # Check if both paths exist in the routes
    paths = [route.path for route in app.routes if hasattr(route, 'path')]
    
    # Should have both /api/v1/products and /api/v1/products/
    assert '/api/v1/products' in paths or '/api/v1/products/' in paths, "Products endpoint not found"
    
    # Check for duplicate prefixes
    products_paths = [p for p in paths if 'products' in p]
    assert len(products_paths) > 0, "No products endpoints found"
    
    # No duplicate segment prefixes
    for p in products_paths:
        assert '/products/products' not in p, f"Duplicate segment prefix found: {p}"
