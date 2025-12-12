<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>내 3D 큐브</title>
    <style>
        /* 화면 테두리 여백 제거 및 스크롤바 숨기기 */
        body { margin: 0; overflow: hidden; background-color: #222; }
        canvas { display: block; } /* 캔버스 하단 공백 제거 */
    </style>
</head>
<body>
    <script type="importmap">
        {
            "imports": {
                "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
                "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
            }
        }
    </script>

    <script type="module">
        import * as THREE from 'three';
        import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

        // --- 기본 설정 (무대, 카메라, 렌더러) ---
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x222222); // 배경색: 진한 회색

        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 5; // 카메라를 뒤로 5만큼 이동

        const renderer = new THREE.WebGLRenderer({ antialias: true }); // 계단현상 방지
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // --- 물체 만들기 (정육면체) ---
        const geometry = new THREE.BoxGeometry(2, 2, 2); 
        // MeshNormalMaterial: 빛이 없어도 보이고, 방향에 따라 색이 예쁘게 변함
        const material = new THREE.MeshNormalMaterial(); 
        const cube = new THREE.Mesh(geometry, material);
        scene.add(cube);

        // --- 마우스 컨트롤 (이게 있어야 마우스로 돌아갑니다) ---
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true; // 부드럽게 멈추는 효과

        // --- 애니메이션 루프 (계속 그리기) ---
        function animate() {
            requestAnimationFrame(animate);
            
            controls.update(); // 마우스 움직임 반영
            renderer.render(scene, camera);
        }
        animate();

        // --- 화면 크기 변경 대응 ---
        window.addEventListener('resize', onWindowResize, false);
        function onWindowResize() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }
    </script>
</body>
</html>
