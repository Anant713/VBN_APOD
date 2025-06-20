import numpy as np
import cv2
def extract_marker_centroids(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Threshold to detect bright blobs
    _, binary = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)

    # Find contours of blobs
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    marker_centroids = []

    # For annotation, convert grayscale image to BGR
    annotated_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    for idx, contour in enumerate(contours):
        mask = np.zeros_like(image)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

        # Weighted centroid calculation
        M = np.mgrid[0:image.shape[0], 0:image.shape[1]]
        weights = image.astype(np.float32) * (mask / 255.0)  # Apply mask

        sum_weights = np.sum(weights)
        if sum_weights > 0:
            cy = np.sum(M[0] * weights) / sum_weights
            cx = np.sum(M[1] * weights) / sum_weights
            marker_centroids.append((cx, cy))

            # Draw a red circle at the centroid
            cv2.circle(annotated_image, (int(cx), int(cy)), 5, (0, 0, 255), -1)

            # Put index label next to the point
            cv2.putText(annotated_image, f'{idx+1}', (int(cx)+5, int(cy)-5), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Save or display the annotated image
    cv2.imwrite("annotated_markers.png", annotated_image)
    # Or to display: cv2.imshow("Annotated", annotated_image); cv2.waitKey(0); cv2.destroyAllWindows()

    return np.array(marker_centroids, dtype=np.float32)

def compute_navigation_solution(led_coords, Df, ymax, zmax, Az_max, El_max):
    """
    led_coords: list of 5 tuples [(x1,y1,z1), ..., (x5,y5,z5)] on camera plane
    Df: focal length constant
    ymax, zmax: pattern size limits
    Az_max, El_max: max Azimuth and Elevation (in radians)
    """

    # Convert to numpy array for easier manipulation
    led_coords = np.array(led_coords)

    # Step 1: Compute center of pattern
    y_c = np.mean(led_coords[:4, 1])
    z_c = np.mean(led_coords[:4, 2])

    # Step 2: Compute relative positions wrt center
    x_prime = led_coords - np.array([0, y_c, z_c])

    # Step 3: Compute Az and El using 4.27
    Az = np.arctan((y_c / ymax) * np.tan(Az_max))
    print(Az)
    El = np.arctan((z_c / zmax) * np.tan(El_max))
    print(El)

    # Step 4: Extract useful values
    x1z = x_prime[0, 2]
    x2z = x_prime[1, 2]
    x4z = x_prime[3, 2]
    x5y = x_prime[4, 1]
    x5z = x_prime[4, 2]
    x3y = x_prime[2, 1]

    # Step 5: Solve for alpha
    alpha = np.arctan2(-x1z, x2z)
    print(alpha)
    # Step 6: Solve for (gamma + Az)
    gamma_plus_Az = np.arcsin((-x5y / (x4z+1e-8)) * np.cos(alpha))
    print(gamma_plus_Az)
    # Step 7: Solve for (beta + El)
    numerator = np.cos(gamma_plus_Az) * np.cos(alpha)
    print(numerator)
    denominator = (x3y / (x5z+1e-8)) + np.sin(gamma_plus_Az) * np.sin(alpha)
    print(denominator)
    beta_plus_El = np.arcsin(numerator / (denominator+1e-8))

    # Step 8: Compute gamma and beta
    gamma = gamma_plus_Az - Az
    beta = beta_plus_El - El

    # Step 9: Compute rotation matrix R123
    def R_123(alpha, beta, gamma):
        ca, cb, cg = np.cos(alpha), np.cos(beta), np.cos(gamma)
        sa, sb, sg = np.sin(alpha), np.sin(beta), np.sin(gamma)

        return np.array([
            [cb * cg, sa * sb * cg - ca * sg, ca * sb * cg + sa * sg],
            [cb * sg, sa * sb * sg + ca * cg, ca * sb * sg - sa * cg],
            [-sb,     sa * cb,                ca * cb]
        ])

    R = R_123(alpha, beta, gamma)
    print(R)

    # Step 10: Compute range R_mag (from 4.30)
    x1y = x_prime[0, 1]
    R_mag = (Df / (x1y+1e-8)) * (
        np.cos(alpha) * np.cos(gamma + Az) - np.sin(alpha) * np.sin(gamma + Az) * np.sin(beta + El)
    )

    # Step 11: Compute s_nc_nc vector (Eq 4.31)
    s_nc_nc = np.array([
        R_mag * np.cos(Az) * np.cos(El),
        R_mag * np.sin(Az) * np.cos(El),
        -R_mag * np.sin(El)
    ])

    # Step 12: Convert to nav frame (Eq 4.32)
    s_nc_n = -R.T @ s_nc_nc

    return {
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "Az": Az,
        "El": El,
        "R123": R,
        "s_nc^n": s_nc_n
    }

# Dummy input (to be replaced with actual values)
led_tuples = [(0.0, 1205.0, 0.0), (0.0, 0.0, 1205.0), (0.0, -1205.0, 0.0), (0.0, 0.0, -1205.0), (0.0, 0.0, 0.0)]
Az_max = np.radians(60)
El_max = np.radians(45)
y_max = 0.2
z_max = 0.2
Df = 0.05

compute_navigation_solution(led_tuples, Df, y_max, z_max, Az_max, El_max)
