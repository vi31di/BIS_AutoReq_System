import asyncio
import json
from api.db import DBConnection, init_db_connection
from api.resolve.resolver import resolve_lookup

async def main():
    await init_db_connection()
    async with DBConnection() as db:
        print("================ VERIFYING FIX 1: Ageing Test ================")
        # Test Case 1: Insulation, Type A, Before Ageing
        res = await resolve_lookup(db, {
            "test_name": "Ageing in air oven",
            "component": "Insulation",
            "category": "Type A",
            "timing": "before"
        })
        print("Insulation Type A Before:", res["value"])
        assert "Min: 12.5" in res["value"] and "Min: 150%" in res["value"]
        
        # Test Case 2: Insulation, Type A, After Ageing
        res = await resolve_lookup(db, {
            "test_name": "Ageing in air oven",
            "component": "Insulation",
            "category": "Type A",
            "timing": "after"
        })
        print("Insulation Type A After:", res["value"])
        assert "Variation Max: ±20%" in res["value"]
        
        # Test Case 3: Sheath, ST1, After Ageing
        res = await resolve_lookup(db, {
            "test_name": "Ageing in air oven",
            "component": "Sheath",
            "category": "ST1",
            "timing": "after"
        })
        print("Sheath ST1 After:", res["value"])
        assert "Variation Max: ±20%" in res["value"]

        print("\n================ VERIFYING FIX 1: Loss of Mass Test ================")
        # Test Case 4: Insulation, Type A, Before
        res = await resolve_lookup(db, {
            "test_name": "Loss of mass test",
            "component": "Insulation",
            "category": "Type A",
            "timing": "before"
        })
        print("Insulation Type A Before:", res["value"])
        assert "N/A" in res["value"]
        
        # Test Case 5: Insulation, Type A, After
        res = await resolve_lookup(db, {
            "test_name": "Loss of mass test",
            "component": "Insulation",
            "category": "Type A",
            "timing": "after"
        })
        print("Insulation Type A After:", res["value"])
        assert "2 mg/cm²" in res["value"]

        # Test Case 6: Insulation, Type C, After
        res = await resolve_lookup(db, {
            "test_name": "Loss of mass test",
            "component": "Insulation",
            "category": "Type C",
            "timing": "after"
        })
        print("Insulation Type C After:", res["value"])
        assert "N/A" in res["value"]

        print("\n================ VERIFYING FIX 2: Shrinkage Test ================")
        # Test Case 8: Insulation Type A
        res = await resolve_lookup(db, {
            "test_name": "Shrinkage test",
            "component": "Insulation",
            "category": "Type A"
        })
        print("Insulation Shrinkage:", res["value"])
        assert "Max Shrinkage: 4%" in res["value"]
        
        # Test Case 9: Sheath ST1
        res = await resolve_lookup(db, {
            "test_name": "Shrinkage test",
            "component": "Sheath",
            "category": "ST1"
        })
        print("Sheath ST1 Shrinkage:", res["value"])
        assert "Max Shrinkage: 4%" in res["value"]

        print("\n================ VERIFYING FIX 4: Thickness Test ================")
        # Test Case 10: Unsheathed Single-Core, Class 2, Size 1.5
        res = await resolve_lookup(db, {
            "test_name": "Thickness of insulation/sheath",
            "component": "Insulation",
            "class": "Class 2",
            "size_mm2": 1.5,
            "construction": "unsheathed_single_core"
        })
        print("Unsheathed Single-Core rigid 1.5:", res["value"])
        assert "0.7 mm" in res["value"]

        # Test Case 11: Sheathed Multi-Core, Class 5, Size 1.5
        res = await resolve_lookup(db, {
            "test_name": "Thickness of insulation/sheath",
            "component": "Insulation",
            "class": "Class 5",
            "size_mm2": 1.5,
            "construction": "sheathed_multi_core"
        })
        print("Sheathed Multi-Core 1.5:", res["value"])
        assert "0.6 mm" in res["value"]

        # Test Case 12: Sheathed Multi-Core Sheath Thickness, Size 1.5
        res = await resolve_lookup(db, {
            "test_name": "Thickness of insulation/sheath",
            "component": "Sheath",
            "size_mm2": 1.5,
            "construction": "sheathed_multi_core"
        })
        print("Sheathed Multi-Core Sheath Thickness 1.5:", res["value"])
        assert "0.8 mm" in res["value"] or "0.9 mm" in res["value"]

        print("\n================ VERIFYING FIX 5: Insulation Resistance ================")
        # Test Case 13: Insulation Type A
        res = await resolve_lookup(db, {
            "test_name": "Insulation resistance test",
            "category": "Type A"
        })
        print("Type A IR Constant:", res["value"])
        assert "36.7 MΩ·km" in res["value"] and "0.037 MΩ·km" in res["value"]

        # Test Case 14: Insulation Type B
        res = await resolve_lookup(db, {
            "test_name": "Insulation resistance test",
            "category": "Type B"
        })
        print("Type B IR Constant:", res["value"])
        assert "36.7 MΩ·km" in res["value"] and "0.37 MΩ·km" in res["value"]

        print("\n================ VERIFYING NEW MATRIX SIMPLIFICATIONS ================")
        # Test Case 16: Hot deformation Insulation Type A
        res = await resolve_lookup(db, {
            "test_name": "Hot deformation test",
            "component": "Insulation",
            "category": "Type A"
        })
        print("Hot Deformation Insulation A:", res["value"])
        assert "80°C" in res["value"] and "50%" in res["value"]
        assert len(res["resolution_path"]) >= 4
        assert res["resolution_path"][0]["address"] == "IS694-2010"
        assert "IS5831-1984" in res["resolution_path"][2]["address"]

        # Test Case 16b: Hot deformation Sheath ST2
        res = await resolve_lookup(db, {
            "test_name": "Hot deformation test",
            "component": "Sheath",
            "category": "ST2"
        })
        print("Hot Deformation Sheath ST2:", res["value"])
        assert "90°C" in res["value"] and "50%" in res["value"]
        assert len(res["resolution_path"]) >= 4

        # Test Case 17: Heat shock Sheath ST1
        res = await resolve_lookup(db, {
            "test_name": "Heat shock test",
            "component": "Sheath",
            "category": "ST1"
        })
        print("Heat Shock Sheath ST1:", res["value"])
        assert "150°C" in res["value"] and "No signs of cracks or scales" in res["value"]
        assert len(res["resolution_path"]) >= 4

        # Test Case 18: Cold bend Insulation Type C
        res = await resolve_lookup(db, {
            "test_name": "Cold bend test",
            "component": "Insulation",
            "category": "Type C"
        })
        print("Cold Bend Insulation C:", res["value"])
        assert "-15°C" in res["value"]
        assert len(res["resolution_path"]) >= 4

        # Test Case 18b: Cold bend Sheath ST2
        res = await resolve_lookup(db, {
            "test_name": "Cold bend test",
            "component": "Sheath",
            "category": "ST2"
        })
        print("Cold Bend Sheath ST2:", res["value"])
        assert "-15°C" in res["value"]
        assert len(res["resolution_path"]) >= 4

        # Test Case 19: Thermal stability Insulation Type C
        res = await resolve_lookup(db, {
            "test_name": "Thermal stability",
            "component": "Insulation",
            "category": "Type C"
        })
        print("Thermal Stability Insulation C:", res["value"])
        assert "80 minutes" in res["value"]
        assert len(res["resolution_path"]) >= 4

        # Test Case 19b: Thermal stability Sheath ST1
        res = await resolve_lookup(db, {
            "test_name": "Thermal stability",
            "component": "Sheath",
            "category": "ST1"
        })
        print("Thermal Stability Sheath ST1:", res["value"])
        assert "40 minutes" in res["value"]

        print("\n================ VERIFYING ANNEALING AND HIGH VOLTAGE FIXES ================")
        # Test Case 20: Annealing test, Copper, 0.15 mm
        res = await resolve_lookup(db, {
            "test_name": "Annealing test (for copper)",
            "material": "Copper",
            "size_mm2": 0.15
        })
        print("Annealing Copper 0.15mm:", res["value"])
        assert "10%" in res["value"]
        assert len(res["resolution_path"]) >= 4

        # Test Case 21: Annealing test, Copper, 0.30 mm
        res = await resolve_lookup(db, {
            "test_name": "Annealing test (for copper)",
            "material": "Copper",
            "size_mm2": 0.30
        })
        print("Annealing Copper 0.30mm:", res["value"])
        assert "15%" in res["value"]

        # Test Case 24: Annealing test, Aluminium
        res = await resolve_lookup(db, {
            "test_name": "Annealing test (for copper)",
            "material": "Aluminium"
        })
        print("Annealing Aluminium:", res["value"])
        assert "25 percent" in res["value"] and "12 percent" in res["value"]
        assert len(res["resolution_path"]) >= 4

        # Test Case 25: HV test, Single-core, Water immersion
        res = await resolve_lookup(db, {
            "test_name": "High voltage test",
            "core_type": "single_core",
            "hv_variant": "water_immersion"
        })
        print("HV Single-core Water Immersion:", res["value"])
        assert "6 kV" in res["value"] and "240 h" in res["value"] and "60±3°C" in res["value"]
        assert len(res["resolution_path"]) >= 2

        # Test Case 26: HV test, Single-core, Room temperature
        res = await resolve_lookup(db, {
            "test_name": "High voltage test",
            "core_type": "single_core",
            "hv_variant": "room_temperature"
        })
        print("HV Single-core Room Temp:", res["value"])
        assert "7.2 kV" in res["value"] and "immersed in water for 1 h" in res["value"]

        # Test Case 27: HV test, Multi-core, Room temperature
        res = await resolve_lookup(db, {
            "test_name": "High voltage test",
            "core_type": "multi_core",
            "hv_variant": "room_temperature"
        })
        print("HV Multi-core Room Temp:", res["value"])
        assert "7.2 kV" in res["value"] and "Ambient" in res["value"] and "immersed" not in res["value"]

        print("\n================ VERIFYING SPLIT TENSILE TESTS ================")
        # Test Case 28: Conductor Tensile, Aluminium Grade 0
        res = await resolve_lookup(db, {
            "test_name": "Tensile strength and elongation at break",
            "component": "Conductor",
            "material": "Aluminium",
            "conductor_grade": "Grade 0"
        })
        print("Tensile Aluminium Grade 0:", res["value"])
        assert "100 N/mm²" in res["value"]
        assert len(res["resolution_path"]) >= 4

        # Test Case 29: Conductor Tensile, Aluminium Grade H2
        res = await resolve_lookup(db, {
            "test_name": "Tensile strength and elongation at break",
            "component": "Conductor",
            "material": "Aluminium",
            "conductor_grade": "Grade H2"
        })
        print("Tensile Aluminium Grade H2:", res["value"])
        assert "150 N/mm²" in res["value"]

        # Test Case 30: Conductor Tensile, Copper (N/A)
        res = await resolve_lookup(db, {
            "test_name": "Tensile strength and elongation at break",
            "component": "Conductor",
            "material": "Copper"
        })
        print("Tensile Copper:", res["value"])
        assert "N/A" in res["value"]

        # Test Case 31: Insulation Tensile Type A
        res = await resolve_lookup(db, {
            "test_name": "Tensile strength and elongation at break",
            "component": "Insulation",
            "category": "Type A"
        })
        print("Tensile Insulation Type A:", res["value"])
        assert "12.5 N/mm²" in res["value"] and "150%" in res["value"]
        assert len(res["resolution_path"]) >= 4

        # Test Case 32: Insulation Tensile Type C
        res = await resolve_lookup(db, {
            "test_name": "Tensile strength and elongation at break",
            "component": "Insulation",
            "category": "Type C"
        })
        print("Tensile Insulation Type C:", res["value"])
        assert "15.0 N/mm²" in res["value"] and "125%" in res["value"]

        # Test Case 33: Sheath Tensile ST1
        res = await resolve_lookup(db, {
            "test_name": "Tensile strength and elongation at break",
            "component": "Sheath",
            "category": "ST1"
        })
        print("Tensile Sheath ST1:", res["value"])
        assert "12.5 N/mm²" in res["value"] and "150%" in res["value"]
        assert len(res["resolution_path"]) >= 4

        print("\nALL FIXES & SIMPLIFICATIONS SUCCESSFULLY VERIFIED!")

if __name__ == "__main__":
    asyncio.run(main())
